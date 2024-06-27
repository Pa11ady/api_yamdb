from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (DjangoFilterBackend,
                                           CharFilter,
                                           FilterSet)
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from reviews.models import Review, Title, Genre, Category
from .permissions import AdminPermission, AdminOrAuthorOrReadOnly
from .serializers import (CommentSerializer,
                          ReviewSerializer,
                          TitleSerializerWrite,
                          TitleSerializerRead,
                          GenreSerializer,
                          CategorySerializer)


class Filter(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


class TitleViewSet(ModelViewSet):
    """Обработчик произведений."""
    http_method_names = ('get', 'patch', 'post', 'delete')
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'name'
    )
    permission_classes = (AdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = Filter

    def get_serializer_class(self):
        if self.request.method in {'POST', 'PATCH'}:
            return TitleSerializerWrite
        return TitleSerializerRead


class GenreListView(ListCreateAPIView):
    """Показ и добавление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreDestroyView(DestroyAPIView):
    """Удаление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'slug'


class CategoryListView(ListCreateAPIView):
    """Показ и добавление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryDestroyView(DestroyAPIView):
    """Удаление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'slug'


class ReviewViewSet(ModelViewSet):
    """Обработчик отзывов."""
    http_method_names = ('get', 'patch', 'post', 'delete')
    serializer_class = ReviewSerializer
    permission_classes = (AdminOrAuthorOrReadOnly,)

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
    permission_classes = (AdminOrAuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'],
                                 title__id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user,
                               review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()
