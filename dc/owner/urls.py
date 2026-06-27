from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OwnerViewSet
from django.urls import path

router = DefaultRouter()

urlpatterns = [
    path('register', OwnerViewSet.as_view({'post': 'register_sub_owner'})),
    path('login', OwnerViewSet.as_view({'post': 'login_sub_owner'})),
    path('subscription', OwnerViewSet.as_view({'get': 'subscription_list'})),
    path('customer', OwnerViewSet.as_view({'get': 'customer_list'})),

    
]