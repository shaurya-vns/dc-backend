from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path('register', UserViewSet.as_view({'post': 'register_user'})),
    path('login', UserViewSet.as_view({'post': 'login_user'})),
    path('change-subowner', UserViewSet.as_view({'post': 'change_subowner'})),
    path('address_add', UserViewSet.as_view({'post': 'address_add'})), 
    path('address_list', UserViewSet.as_view({'get': 'address_list'})), 
    path('address_update', UserViewSet.as_view({'put': 'address_update'})), 
    path('address_delete', UserViewSet.as_view({'delete': 'address_delete'})), 
    path('address_default', UserViewSet.as_view({'get': 'address_default'})), 

    
]