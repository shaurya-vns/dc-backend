from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet
from django.urls import path

router = DefaultRouter()

urlpatterns = [
    path("register", VendorViewSet.as_view({"post": "register_vendor"})),
]