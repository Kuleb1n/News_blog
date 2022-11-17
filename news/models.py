from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField('Heading', max_length=150)
    slug = models.SlugField('URL', max_length=300, unique=True, db_index=True)
    content = models.TextField('Content')
    created_at = models.DateTimeField('Date of publication', auto_now_add=True)
    updated_at = models.DateTimeField('Publication update date', auto_now=True)
    photo = models.ImageField('Photo', upload_to='photo/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField('Published', default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

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
