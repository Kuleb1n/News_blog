from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsIndex.as_view(), name='index'),
    path('delete/<slug:news_slug>/', DeleteNews.as_view(), name='delete'),
    path('category/<slug:category_slug>/', ShowNewsByCategory.as_view(), name='show_category'),
    path('news/<slug:news_slug>/', ShowNews.as_view(), name='show_news'),
    path('news-update/<slug:news_slug>/', UpdateNews.as_view(), name='news-update'),
    path('add_news/', AddNews.as_view(), name='add_news'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_us, name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUser.as_view(), name='profile_change'),
    path('accounts/password/change/', PasswordChange.as_view(), name='password_change'),
    path('show/profile/<int:user_pk>/', ShowProfile.as_view(), name='show_profile'),
]
