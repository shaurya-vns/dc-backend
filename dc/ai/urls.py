from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AIViewSet
from django.urls import path

router = DefaultRouter()


urlpatterns = [
    path('chat-stream', AIViewSet.as_view({'post': 'chat_stream'})),
    #path('recommend-product', AIViewSet.as_view({'post': 'recommend_product'})),
    #path('smart-search', AIViewSet.as_view({'post': 'smart_search'})),
]