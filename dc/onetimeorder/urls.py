from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OneTimeOrderViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path("create", OneTimeOrderViewSet.as_view({"post": "create_order"})),
    path("my_orders", OneTimeOrderViewSet.as_view({"get": "my_orders"})),
    path("order_detail", OneTimeOrderViewSet.as_view({"get": "order_detail"})),
    path("today_orders", OneTimeOrderViewSet.as_view({"get": "today_orders"})),
]