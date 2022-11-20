from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsIndex.as_view(), name='index'),
    path('category/<slug:category_slug>/', ShowNewsByCategory.as_view(), name='show_category'),
    path('news/<slug:news_slug>/', ShowNews.as_view(), name='show_news'),
    path('add_news/', AddNews.as_view(), name='add_news'),
]
