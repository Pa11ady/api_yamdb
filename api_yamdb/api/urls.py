from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()

router.register('titles', views.TitleViewSet)
router.register(r'titles/(?P<title_id>[^/.]+)',
                views.ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)',
                views.CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('genres/', views.GenreListView.as_view()),
    path('genres/<slug:slug>/', views.GenreDestroyView.as_view()),
    path('categories/', views.CategoryListView.as_view()),
    path('categories/<slug:slug>/', views.CategoryDestroyView.as_view()),
]
