from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SupportViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [

    # Customer
    path(
        "tickets/create",
        SupportViewSet.as_view({"post": "create_ticket"}),
    ),

    path(
        "tickets",
        SupportViewSet.as_view({"get": "my_tickets"}),
    ),

    path(
        "tickets/detail",
        SupportViewSet.as_view({"get": "ticket_detail"}),
    ),

    path(
        "tickets/send-message",
        SupportViewSet.as_view({"post": "send_message"}),
    ),

    path(
        "tickets/messages",
        SupportViewSet.as_view({"get": "ticket_messages"}),
    ),

    path(
        "tickets/close",
        SupportViewSet.as_view({"put": "close_ticket"}),
    ),
]