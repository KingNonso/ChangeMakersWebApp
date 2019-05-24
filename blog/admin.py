from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Image, Media, Comment, Video, Category


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1
    fields = ('image', 'description')
    # readonly_fields = ('image_tag',)


class VideoInline(admin.StackedInline):
    model = Video
    extra = 1
    fields = ('video', 'description')
    # readonly_fields = ('video_tag',)


class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug', 'top_story', 'status', 'views', 'last_seen')
    list_filter = ['date', 'category']
    list_editable = ('top_story', 'category', 'status')
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = [
        (None, {'fields': ['title', 'slug', 'body', 'category', 'status', 'top_story', 'tags']}),
        ('Event/ Publication Date', {'fields': ['date'], 'classes': ['collapse']}),
    ]
    inlines = [ImageInline, VideoInline]


admin.site.register(Media, MediaAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
