from django.urls import include, path
from rest_framework import routers

from .views import GetTokenAPIView, RegistrationAPIView, UserViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls), name='users'),
    path('auth/signup/', RegistrationAPIView.as_view(), name='signup'),
    path('auth/token/', GetTokenAPIView.as_view(), name='token'),
]
