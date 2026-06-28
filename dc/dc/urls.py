

from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
  
# Create the Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="POC Python API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@myapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/',include('users.urls')),
    path('api/subowner/',include('owner.urls')),
    path('api/product/',include('product.urls')),
    path('api/subscription/',include('subscription.urls')),
    path('api/order/',include('order.urls')),
    path('api/delivery/',include('delivery.urls')),
    path('api/dashboard/',include('dashboard.urls')),
    path('api/reviews/',include('reviews.urls')),
    

   
   # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

]
