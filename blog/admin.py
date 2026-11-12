from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'featured', 'published', 'created_at')
    list_filter = ('published', 'featured', 'category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    list_editable = ('featured', 'published')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Conteúdo', {
            'fields': ('content', 'image_url')
        }),
        ('Configurações', {
            'fields': ('published', 'featured')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'content')
