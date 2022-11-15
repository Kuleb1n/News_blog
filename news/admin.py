from django.contrib import admin
from .models import News, Category


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'content', 'created_at', 'updated_at', 'photo', 'is_published']
    list_display_links = ['id', 'title']
    list_filter = ['title', 'created_at', 'updated_at', 'is_published', 'category']
    search_fields = ['title', 'content']
    list_editable = ['is_published']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    list_filter = ['title']
    search_fields = ['title']


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
