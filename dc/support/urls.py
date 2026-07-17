from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SupportViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path("tickets/create_update", SupportViewSet.as_view({"post": "create_update_ticket"})),
    path("tickets/get", SupportViewSet.as_view({"get": "get_ticket_by_order"})),
]