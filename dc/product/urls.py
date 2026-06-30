from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [
    path('create', ProductViewSet.as_view({'post': 'create_product'})),
    path('list', ProductViewSet.as_view({'get': 'product_list'})),
    path('product_detail', ProductViewSet.as_view({'get': 'product_detail'}))
]