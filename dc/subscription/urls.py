from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path('create', SubscriptionViewSet.as_view({'post': 'create_subscription'})),
    path('me', SubscriptionViewSet.as_view({'get': 'my_subscriptions'})),
    path('detail', SubscriptionViewSet.as_view({'get': 'subscriptions_detail'})),
    path("pause", SubscriptionViewSet.as_view({"get": "subscriptions_pause"})),
    path("resume", SubscriptionViewSet.as_view({"get": "subscriptions_cancelled"})),
    path("cancel", SubscriptionViewSet.as_view({"get": "subscriptions_resume"})),
]