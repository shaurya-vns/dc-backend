from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path('register', UserViewSet.as_view({'post': 'register_user'})),
    path('login', UserViewSet.as_view({'post': 'login_user'})),
    path('change-subowner', UserViewSet.as_view({'post': 'change_subowner'})), 
    path('profile', UserViewSet.as_view({'get': 'get_profile'})), 
    path('update', UserViewSet.as_view({'put': 'update_profile'})), 
    path('all', UserViewSet.as_view({'get': 'get_all_profile'})),     
]