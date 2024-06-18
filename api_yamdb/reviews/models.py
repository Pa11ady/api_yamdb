from django.db import models

MAX_LENGTH = 256


class Genre(models.Model):
    """Модель описывающая жанр."""
    name = models.TextField(verbose_name='Жанр')
    slug = models.SlugField(unique=True, verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(models.Model):
    """Модель описывающая категорию."""
    name = models.TextField(verbose_name='Категория')
    slug = models.SlugField(unique=True, verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Модель описывающая произведение."""
    name = models.TextField(max_length=MAX_LENGTH, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(verbose_name='Описание')
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='Slug жанра')
    category = models.OneToOneField(
        Category, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='Slug категории')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
