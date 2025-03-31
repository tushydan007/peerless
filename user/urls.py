from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,LoginView, LogoutView


router = DefaultRouter()
router.register('user', UserViewSet, basename='user')

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
] + router.urls