from django.db import models

from users.models import User

MAX_LENGTH_NAME: int = 256
MAX_LENGTH_SLUG: int = 50


class Genre(models.Model):
    """Модель описывающая жанр."""
    name = models.TextField(max_length=MAX_LENGTH_NAME,
                            verbose_name='Жанр')
    slug = models.SlugField(max_length=MAX_LENGTH_SLUG, unique=True,
                            verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель описывающая категорию."""
    name = models.TextField(max_length=MAX_LENGTH_NAME,
                            verbose_name='Категория')
    slug = models.SlugField(max_length=MAX_LENGTH_SLUG, unique=True,
                            verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель описывающая произведение."""
    name = models.TextField(max_length=MAX_LENGTH_NAME,
                            verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(verbose_name='Описание', blank=True)
    genre = models.ManyToManyField(
        Genre, verbose_name='Slug жанра', blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Slug категории')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель описывающая отзыв."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Текст отзыва')
    score = models.PositiveIntegerField('Оценка', blank=False)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    db_index=True)

    class Meta:
        constraints = (models.UniqueConstraint(fields=('author', 'title'),
                                               name='one_author_for_title'),)

        ordering = ('pub_date', )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'отзывы'
        default_related_name = 'reviews'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель описывающая комментарий."""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField('Дата комментария', auto_now_add=True,
                                    db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('pub_date', )
        default_related_name = 'comments'

    def __str__(self):
        return self.review
