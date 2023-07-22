import scrapy
from itemadapter import ItemAdapter
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess

from utils.migration import create_author, create_post
from .models import Author


class QuoteItem(Item):
    quote = Field()
    author = Field()
    tags = Field()


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuotesPipline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if 'fullname' in adapter.keys():
            name = ['Alexandre Dumas fils' if adapter['fullname'] == 'Alexandre Dumas-fils'  else adapter['fullname']]
            author_data = {
                'fullname': name,
                'born_date': adapter['born_date'],
                'born_location': adapter['born_location'],
                'description': adapter['description'],
            }
            author = create_author(author_data)

        if 'quote' in adapter.keys():
            post_data = {
                'quote': adapter['quote'],
                'tags': adapter['tags'],
                'author': adapter['author'],
            }
            post = create_post(post_data)


        return item


class QuotesSpider(scrapy.Spider):
    name = "to_scrapy"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {"ITEM_PIPELINES": {
        QuotesPipline: 300,
    },'LOG_LEVEL' : 'WARNING'}

    def parse(self, response, **kwargs):
        for quote in response.xpath("/html//div[@class='quote']"):
            text = quote.xpath("span[@class='text']/text()").get().strip()
            author = quote.xpath("span/small[@class='author']/text()").get().strip()
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            yield QuoteItem(quote=text, author=author, tags=tags)
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get(),
                                  callback=self.parse_author)
        next_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response, **kwargs):  # noqa
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath('h3[@class="author-title"]/text()').get().strip()
        date_born = content.xpath('p/span[@class="author-born-date"]/text()').get().strip()
        location_born = content.xpath('p/span[@class="author-born-location"]/text()').get().strip()
        bio = content.xpath('div[@class="author-description"]/text()').get().strip()
        yield AuthorItem(fullname=fullname, born_date=date_born, born_location=location_born, description=bio)

class AuthorsSpider(scrapy.Spider):
    name = "authors_scrapy"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response, **kwargs):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get(),
                                  callback=self.parse_author)
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response, **kwargs):
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath('h3[@class="author-title"]/text()').get().strip()
        date_born = content.xpath('p/span[@class="author-born-date"]/text()').get().strip()
        location_born = content.xpath('p/span[@class="author-born-location"]/text()').get().strip()
        bio = content.xpath('div[@class="author-description"]/text()').get().strip()
        yield AuthorItem(fullname=fullname, born_date=date_born, born_location=location_born, description=bio)


def scrapping_authors():
    process = CrawlerProcess()
    process.crawl(AuthorsSpider)
    process.start()


def scrapping_quotes():
    proces = CrawlerProcess()
    proces.crawl(QuotesSpider)
    proces.start()


if __name__ == '__main__':
    scrapping_authors()
    scrapping_quotes()