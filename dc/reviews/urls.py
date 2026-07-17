from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path('create', ReviewViewSet.as_view({'post': 'create_review'})),
    path('list', ReviewViewSet.as_view({'get': 'product_review_list'})),
]