from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Author, Post, Tag
from users.models import Quote as UserPost, Author as UserAuthor
from bson import ObjectId

def main(request, page=1):
    per_page = 10

    user_quotes = UserPost.objects.all()
    other_quotes = Post.objects.all()

    quotes = list(user_quotes) + list(other_quotes)
    quotes.sort(key=lambda q: q.id)

    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


def quotes_by_tag(request, tag_name):
    user_quotes = UserPost.objects.filter(tags__name=tag_name)
    other_quotes = Post.objects.filter(tags__name=tag_name)

    quotes = list(user_quotes) + list(other_quotes)
    quotes.sort(key=lambda q: q.id)

    return render(request, 'quotes/index.html', {'quotes': quotes})


def author_detail_view(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        author = UserAuthor.objects.get(id=author_id)
    return render(request, 'authors/author_detail.html', {'author': author})
