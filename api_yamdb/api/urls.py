from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()

router.register('titles', views.TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet,
                basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('genres/', views.GenreListView.as_view()),
    path('genres/<slug:slug>/', views.GenreDestroyView.as_view()),
    path('categories/', views.CategoryListView.as_view()),
    path('categories/<slug:slug>/', views.CategoryDestroyView.as_view()),
]
