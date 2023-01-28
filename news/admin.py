from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import News, Category, User, RatingStar, Rating


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'content', 'created_at', 'updated_at', 'get_photo', 'is_published',
                    'slug', 'user']
    list_display_links = ['id', 'title']
    list_filter = ['title', 'created_at', 'updated_at', 'is_published', 'category']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    prepopulated_fields = {"slug": ("title",)}
    fields = (
        'title', 'slug', 'category', 'content', 'photo', 'get_photo', 'updated_at', 'created_at', 'is_published',
        'user')
    readonly_fields = ('get_photo', 'updated_at', 'created_at')
    actions = ['make_published', 'make_unpublished']

    @admin.action(description='Mark selected news as published')
    def make_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request,
                          'The selected news has been published.\n'
                          f'Number of added publications: {count}')

    @admin.action(description='Mark selected news unpublished')
    def make_unpublished(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request,
                          'The selected news has been transferred ti the unpublished status.\n'
                          f'Number of removed publications: {count}',
                          messages.ERROR
                          )

    def get_photo(self, object):
        return mark_safe(f"<img src='{object.photo.url}' width=100")

    get_photo.short_description = 'Photo'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    list_display_links = ['id', 'title']
    list_filter = ['title']
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title",)}


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'short_status', 'get_photo', 'date_joined',
                    'is_staff']
    list_display_links = ['username', 'email']
    search_fields = ['username', 'email', 'last_name']
    list_filter = ['date_joined']
    fields = ('username', 'email', 'short_status', 'first_name', 'last_name', 'user_photo', 'get_photo',
              'is_staff', 'is_active', 'is_superuser')
    readonly_fields = ('get_photo',)

    def get_photo(self, object):
        return mark_safe(f"<img src='{object.user_photo.url}' width=100")

    get_photo.short_description = "User_photo"


class RatingStarAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'star', 'user', 'news', 'rating_date']
    fields = ('news', 'user', 'star')


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(RatingStar, RatingStarAdmin)
admin.site.register(Rating, RatingAdmin)
