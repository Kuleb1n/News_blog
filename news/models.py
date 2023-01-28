from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    title = models.CharField('Heading', max_length=150)
    slug = models.SlugField('URL', max_length=300, unique=True, db_index=True)
    content = models.TextField('Content')
    created_at = models.DateTimeField('Date of publication', auto_now_add=True)
    updated_at = models.DateTimeField('Publication update date', auto_now=True)
    photo = models.ImageField('Photo', upload_to='photo/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField('Published', default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('show_news', kwargs={'news_slug': self.slug})


class Category(models.Model):
    title = models.CharField('Category', max_length=120, db_index=True)
    slug = models.SlugField('URL', max_length=120, unique=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('show_category', kwargs={'category_slug': self.slug})


class User(AbstractUser):
    email = models.EmailField(_("Email address"), unique=True)
    short_status = models.CharField('Status', blank=True, max_length=100)
    user_photo = models.ImageField('User photo', upload_to='users/%Y/%m/%d/', default='user_def.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'user_pk': self.pk})


class RatingStar(models.Model):
    value = models.SmallIntegerField('Rating value', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Rating value'
        verbose_name_plural = 'Rating values'
        ordering = ['-value']


class Rating(models.Model):
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Star')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Rated by the user')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Rating to the news')
    rating_date = models.DateTimeField('Rating date', auto_now=True)

    def __str__(self):
        return f'{self.star} - {self.news}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
