from django.contrib import admin

from .models import Category, Post, Location, Comment


@admin.action(description='Снять с публикации')
def published_false(modelAdmin, request, queryset):
    queryset.update(is_published=False)

@admin.action(description='Поставить на публикацию')
def published_true(modelAdmin, request, queryset):
    queryset.update(is_published=True)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    actions = [
        published_true,
        published_false,
    ]
    list_display = (
        'title',
        'text_short',
        'is_published',
        'category',
        'author',
        'created_at',
    )
    list_display_links = ('title',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('category',)
    list_per_page = 10
    raw_id_fields = ('category',)
    fieldsets = [
        (None, {
            'fields': ('title', 'text', 'pub_date',),
        }),
        ('Photo', {
            'fields': ('image',),
            'classes': ('collapse',),
            'description': 'Фотография публикации, можно изменить и удалить'
        }),
        ('Is_published', {
            'fields': ('is_published',),
            'classes': ('collapse',),
            'description': 'Опубликовать публикацию или снять с публикации'
        })
    ]

    def text_short(self, obj: Post):
        if len(obj.text) < 48:
            return obj.text
        else:
            return obj.text[:48] + '...'


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
