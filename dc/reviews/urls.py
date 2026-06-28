from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path('create_review', ReviewViewSet.as_view({'post': 'create_review'})),
    path('product_reviews', ReviewViewSet.as_view({'get': 'product_reviews'})),
    path('subowner_reviews', ReviewViewSet.as_view({'get': 'subowner_reviews'})),
]