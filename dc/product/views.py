 
 
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

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
 

from .models import ProductModel
from .serializers import (
    ProductListSerializer,
    ProductCreateSerializer
)

 
class ProductViewSet(viewsets.ViewSet):
        
        @swagger_auto_schema(
        request_body=ProductCreateSerializer,
        tags=["Product"]
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
            tags=["Product"]
        )
        @action(detail=False, methods=['get'])
        def product_list(self, request):
            try:
                queryset = ProductModel.objects.filter(
                    is_active=True
                ).order_by("-created_at")

                serializer = ProductListSerializer(
                    queryset,
                    many=True
                )

                return response_fun(RESPONSE_SUCCESS, {'data':serializer.data})

            except Exception as e:
                return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 

