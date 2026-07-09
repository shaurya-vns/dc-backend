from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AddressViewSet
from django.urls import path

router = DefaultRouter()

urlpatterns = [

    path("add", AddressViewSet.as_view({"post": "address_add"})),
    path("list", AddressViewSet.as_view({"get": "address_list",})),
    path("delete", AddressViewSet.as_view({"delete": "address_delete"})),
    path("update", AddressViewSet.as_view({"put": "address_update" })),
    path("default", AddressViewSet.as_view({"get": "address_default"})),
]