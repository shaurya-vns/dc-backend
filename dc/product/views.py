 
 
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .serializers import *
from dc.utils import response_fun
from dc.constant import RESPONSE_INVALID, RESPONSE_SUCCESS, RESPONSE_ERROR
from dc.errors import ERROR_CODE_UNAUTHORIZED, ERROR_CODE_NOT_FOUND
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers        import make_password
from dc.parameters import TOKEN
from dc.utils import authenticate_and_get_user
from dc.errors import *
from dc.parameters import *

from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Exists, OuterRef
from subscription.models import SubscriptionModel
 
from dc.constant import *

from .models import ProductModel
from .serializers import (
    ProductCreateSerializer
)

 
class ProductViewSet(viewsets.ViewSet):
        
        @swagger_auto_schema(
        request_body=ProductCreateSerializer,
        tags=["Product"],
        operation_description="Create product by subowner",
        )
        @action(detail=False, methods=["post"])
        def create_product(self, request):
            try:
                serializer = ProductCreateSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return response_fun(RESPONSE_SUCCESS, {
                        'message': 'Product created successfully',
                        'data': serializer.data
                    })

                return response_fun(RESPONSE_INVALID, {'errors': serializer.errors,'code': ERROR_CODE_BAD_REQUEST})

            except Exception as e:
               print('eeeee ', e)
               return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 

        @swagger_auto_schema(
            tags=["Product"],
            operation_description="List of all products",
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=['get'])
        def product_list(self, request):
            try:
                queryset = ProductModel.objects.filter(
                    is_active=True
                ).select_related(
                    "vendor",
                    "offer"
                ).prefetch_related(
                    "pricing_options",
                    "vendor__addresses",
                ).order_by("-created_at")

                serializer = ProductDetailSerializer(
                    queryset,
                    many=True
                )

                return response_fun(RESPONSE_SUCCESS, {'data':serializer.data})

            except Exception as e:
                print('eeeee ',e)
                return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
            


        @swagger_auto_schema(
            tags=["Product"],
            operation_description="Full Product Detail with SubOwner",
            manual_parameters=[TOKEN, PRODUCT_ID]
        )
        @action(detail=False, methods=["get"])
        def product_detail(self, request):
            try:

                print('request ', request)
                user, error = authenticate_and_get_user(request)
                print('request user ', user)
               

                if error:
                    return error

                product_id = request.query_params.get("productId")

                if not product_id:
                    return response_fun(RESPONSE_INVALID, {
                        "message": "product_id is required",
                        "code": ERROR_CODE_BAD_REQUEST
                    })

                product = ProductModel.objects.filter(
                    id=product_id,
                    is_active=True
                ).select_related(
                    "vendor",
                    "offer"
                ).prefetch_related(
                    "pricing_options",
                    "vendor__addresses",
                ) .annotate(
                        isSubscribed=Exists(
                            SubscriptionModel.objects.filter(
                                user=user,
                                status= ACTIVE,
                                product=OuterRef("pk")
                            )
                        )
                ).first()

                if not product:
                    return response_fun(RESPONSE_INVALID, {
                        "message": "Product not found",
                        "code": ERROR_CODE_NOT_FOUND
                    })

                serializer = ProductDetailSerializer(product)

                return response_fun(RESPONSE_SUCCESS, {
                    "data": serializer.data
                })

            except Exception as e:
                print("eeeee", e)
                return response_fun(RESPONSE_INVALID, {
                    "message": "Something went wrong !!",
                    "code": ERROR_CODE_NOT_FOUND
                })
