from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DeliveryViewSet
from django.urls import path

router = DefaultRouter()

urlpatterns = [
    path('register', DeliveryViewSet.as_view({'post': 'register_delivery'})),
    path('list', DeliveryViewSet.as_view({'get': 'list_partner'})),
]