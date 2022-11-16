from django.shortcuts import render
from .models import News, Category


def index(request):
    news = News.objects.all()
    categories = Category.objects.all()
    content = {
        'news': news,
        'categories': categories,
    }
    return render(request, 'news/index.html', content)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    content = {
        'news': news,
        'categories': categories,
        'category': category,
    }
    return render(request, 'news/category.html', content)


