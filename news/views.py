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
