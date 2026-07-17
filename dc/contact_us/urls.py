from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ContactUsViewSet
from django.urls import path

router = DefaultRouter()

urlpatterns = [
    path("user/create", ContactUsViewSet.as_view({"post": "user_create"})),
    path("user/list", ContactUsViewSet.as_view({"get": "user_request_list"})),
    path("user/detail", ContactUsViewSet.as_view({"get": "user_detail"})),
    path("admin/list", ContactUsViewSet.as_view({"get": "admin_list"})),
    path("admin/update/<int:pk>", ContactUsViewSet.as_view({"put": "admin_update_status"})),
]