from django.contrib import admin
from .models import Category, Tag, Post, PostImage, Like, Comment, CommentLike, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'anonymity', 'is_pinned', 'view_count', 'like_count', 'comment_count', 'created_at')
    list_filter = ('is_pinned', 'anonymity', 'category', 'created_at')
    search_fields = ('title', 'content')
    inlines = [PostImageInline]
    raw_id_fields = ('author', 'category')
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'anonymity', 'is_deleted', 'created_at')
    list_filter = ('anonymity', 'is_deleted', 'created_at')
    search_fields = ('content',)
    raw_id_fields = ('post', 'author', 'parent')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
