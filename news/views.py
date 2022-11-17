from django.shortcuts import render, get_object_or_404
from .models import News, Category


def index(request):
    news = News.objects.filter(is_published=True)
    content = {
        'news': news,
    }
    return render(request, 'news/index.html', content)


def show_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    news = News.objects.filter(category_id=category.pk)
    content = {
        'news': news,
        'category': category,
    }
    return render(request, 'news/category.html', content)


def show_news(request, news_slug):
    news = get_object_or_404(News, slug=news_slug)
    content = {
        'news': news,
    }
    return render(request, 'news/show_news.html', content)
