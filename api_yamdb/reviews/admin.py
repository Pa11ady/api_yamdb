from django.contrib import admin

from .models import Category, Genre, Review, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')
    list_filter = ('year', 'category')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'score', 'pub_date', 'title')
    list_filter = ('pub_date', 'score', 'title')
    search_fields = ('author', 'text')
    readonly_fields = ('pub_date',)

    autocomplete_fields = ('author', 'title')
