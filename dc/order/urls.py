from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path("list", OrderViewSet.as_view({"get": "subscription_user_order_list"})),
    path("me", OrderViewSet.as_view({"get": "subscription_me_order_list"})),
    path('update', OrderViewSet.as_view({'put': 'update_sub_order_status'})),
]