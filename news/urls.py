from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('category/<slug:category_slug>/', show_category, name='show_category'),
    path('news/<slug:news_slug>/', show_news, name='show_news'),
]
