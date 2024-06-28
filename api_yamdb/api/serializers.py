from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

MIN_SCORE: int = 1
MAX_SCORE: int = 10


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериализатор произведения чтение."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title


class TitleSerializerWrite(serializers.ModelSerializer):
    """Сериализатор произведения запись."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True
    )
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year = date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть в будущем!'
            )
        return value

    def to_representation(self, instance):
        return TitleSerializerRead(instance).data

    def validate_genre(self, value):
        if not value:
            raise serializers.ValidationError(
                'Заполните список жанров!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзыва."""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title = get_object_or_404(
                Title,
                id=self.context['view'].kwargs.get('title_id')
            )
            author = self.context['request'].user
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв к этому произведению!'
                )
        return data

    def validate_score(self, score):
        if not MIN_SCORE <= score <= MAX_SCORE:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10!')
        return score


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментария."""
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
