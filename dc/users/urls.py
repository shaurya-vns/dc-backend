from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path('register', UserViewSet.as_view({'post': 'register_user'})),
    path('login', UserViewSet.as_view({'post': 'login_user'})),
    path('change-subowner', UserViewSet.as_view({'post': 'change_subowner'})),
]