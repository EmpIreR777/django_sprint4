from django.contrib import admin

from .models import Category, Post, Location, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text',
                    'is_published', 'category',
                    'author', 'created_at')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('category',)
    list_per_page = 10
    raw_id_fields = ('category',)


class PostInLine(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInLine,)
    list_display = ('title', 'description', 'slug')


class PostInLine(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInLine,)
    list_display = ('name', 'is_published', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')


admin.site.empty_value_display = 'Не задано'
