from django.db import models


class News(models.Model):
    title = models.CharField('Heading', max_length=150)
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


class Category(models.Model):
    title = models.CharField('Category', max_length=120, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']
