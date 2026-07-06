from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OneTimeOrderViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path("create", OneTimeOrderViewSet.as_view({"post": "create_order"})),
    path("list", OneTimeOrderViewSet.as_view({"get": "user_one_time_order_list"})),
    path('update', OneTimeOrderViewSet.as_view({'put': 'update_onetime_order_status'})), 
]