from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path("list", OrderViewSet.as_view({"get": "subscription_user_order_list"})),
    path("vendor/<int:pk>/reject", OrderViewSet.as_view({"put": "vendor_reject"})),
    path("user/<int:pk>/cancel", OrderViewSet.as_view({"put": "user_cancel"})),
    path("vendor/<int:pk>/delivery", OrderViewSet.as_view({"put": "vendor_delivery"})),
]