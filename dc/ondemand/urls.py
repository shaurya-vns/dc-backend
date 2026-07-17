from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import path
router = DefaultRouter()
from django.urls import path
from .views import OnDemandViewSet

urlpatterns = [
    path("create", OnDemandViewSet.as_view({"post": "create"})),
    path("list", OnDemandViewSet.as_view({"get": "on_demand_list"})),
    path("user/<int:pk>/cancel", OnDemandViewSet.as_view({"put": "user_cancel"})),
    path("user/<int:pk>/approve", OnDemandViewSet.as_view({"put": "user_approve"})),

    path("vendor/<int:pk>/reject", OnDemandViewSet.as_view({"put": "vendor_reject"})),
    path("vendor/<int:pk>/approve", OnDemandViewSet.as_view({"put": "vendor_approve"})),
    path("vendor/<int:pk>/amount", OnDemandViewSet.as_view({"put": "vendor_update_amount"})),
    path("vendor/<int:pk>/payment", OnDemandViewSet.as_view({"put": "vendor_approve_payment"})),

    path("vendor/<int:pk>/delivery", OnDemandViewSet.as_view({"put": "vendor_delivery"})),
]