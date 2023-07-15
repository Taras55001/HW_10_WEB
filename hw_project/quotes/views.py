from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
from .utils import get_mongodb
from utils.models import Autor, Post, Tag

def main(request, page=1):
    db = get_mongodb()
    quotes = Post.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes':quotes_on_page})