from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DeliveryViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path("update-status", DeliveryViewSet.as_view({"post": "update_order_status"})),    
]