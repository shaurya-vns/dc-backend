from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DashboardViewSet
from django.urls import path,include

router = DefaultRouter()

urlpatterns = [

    path("login", DashboardViewSet.as_view({"post": "login_admin_user"})),  
    path("summary", DashboardViewSet.as_view({"get": "get_dashboard"})),  
    path("today-orders", DashboardViewSet.as_view({"get": "today_orders"})),  
    path("subowners", DashboardViewSet.as_view({"get": "get_subowner_list"})),  
]