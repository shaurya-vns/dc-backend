from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path("my-orders", OrderViewSet.as_view({"get": "my_orders"})),
    path("order-detail", OrderViewSet.as_view({"get": "order_detail"})),
    path("upcoming-orders", OrderViewSet.as_view({"get": "upcoming_orders"})),
    path("today-orders", OrderViewSet.as_view({"get": "today_orders"})),
    path("next-day-order", OrderViewSet.as_view({"get": "next_day_orders"})),
    path("subscription", OrderViewSet.as_view({"get": "get_order_by_subscription_id"})),
    path("history", OrderViewSet.as_view({"get": "order_history"})),
]