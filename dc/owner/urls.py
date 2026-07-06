from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OwnerViewSet
from django.urls import path

router = DefaultRouter()

urlpatterns = [
    path("register/", OwnerViewSet.as_view({"post": "register_sub_owner"})),
    path("login/", OwnerViewSet.as_view({"post": "login_sub_owner"})),

    # 📍 ADDRESSES (REST STYLE)
    path("addresses/", OwnerViewSet.as_view({"get": "address_list", "post": "address_add"})),

    path("addresses/<int:pk>/", OwnerViewSet.as_view({
        "put": "address_update",
        "delete": "address_delete"
    })),

    path("addresses/default/", OwnerViewSet.as_view({"get": "address_default"})),

    # 📦 SUBSCRIPTIONS
    path("subscriptions/", OwnerViewSet.as_view({"get": "subscriptions_list_by_user_id"})),
]