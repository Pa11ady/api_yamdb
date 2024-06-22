from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination

from reviews.models import Review, Title, Genre, Category
from .serializers import (CommentSerializer,
                          ReviewSerializer,
                          TitleSerializer,
                          GenreSerializer,
                          CategorySerializer)


class TitleViewSet(ModelViewSet):
    """Обработчик произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination


class GenreListView(ListCreateAPIView):
    """Показ и добавление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDestroyView(DestroyAPIView):
    """Удаление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class CategoryListView(ListCreateAPIView):
    """Показ и добавление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDestroyView(DestroyAPIView):
    """Удаление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ReviewViewSet(ModelViewSet):
    """Обработчик отзывов."""
    http_method_names = ('get', 'patch', 'post', 'delete')
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user,
                               title=self.get_title())

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(ModelViewSet):
    """Обработчик комментариев."""
    http_method_names = ('get', 'patch', 'post', 'delete')
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'],
                                 title__id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user,
                               review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()
