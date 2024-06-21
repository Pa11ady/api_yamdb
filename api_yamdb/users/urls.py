from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, UserCreateViewSet, UserReceiveTokenViewSet)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

auth_urls = [
    path('signup/',
         UserCreateViewSet.as_view({'post': 'create'}),
         name='signup'),
    path('token/',
         UserReceiveTokenViewSet.as_view({'post': 'create'}),
         name='token')
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urls))
]
