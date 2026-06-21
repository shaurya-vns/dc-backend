from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path('register', CustomerViewSet.as_view({'post': 'register'})),
    path('login', CustomerViewSet.as_view({'post': 'login'})),
]