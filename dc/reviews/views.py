 
 
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
from django.db.models import Avg, Count

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from reviews.service import ReviewService
 

from .models import ProductModel
from product.serializers import (
    ProductListSerializer,
    ProductCreateSerializer
)

class ReviewViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        tags=["Reviews"],
        request_body=ReviewCreateSerializer,
        manual_parameters=[TOKEN],
    )
    @action(detail=False, methods=["post"])
    def create_review(self, request):

        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error

            if user.userType != UserModel.USER:

                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Only user can review.",
                        "code": ERROR_CODE_BAD_REQUEST,
                    },
                )

            serializer = ReviewCreateSerializer(
                data=request.data
            )

            if not serializer.is_valid():

                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "errors": serializer.errors,
                        "code": ERROR_CODE_BAD_REQUEST,
                    },
                )

            review = ReviewService.create_or_update_review(user, serializer.validated_data)

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "message": "Review submitted successfully.",
                },
            )

        except Exception as e:
            print('ssss ', e)

            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": str(e),
                    "code": ERROR_CODE_BAD_REQUEST,
                },
            )
        
    @swagger_auto_schema(
    tags=["Reviews"],
        manual_parameters=[TOKEN, PRODUCT_ID],
    )
    @action(detail=False, methods=["get"])
    def product_review_list(self, request):
        try:

            product_id = request.query_params.get("productId")

            if not product_id:
                return response_fun(
                    RESPONSE_INVALID,
                    {"message": "Product Id is required."},
                )

            reviews = ReviewModel.objects.filter(
                product_id = product_id
            )

            serializer = ReviewSerializer(reviews, many=True)

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    'data': serializer.data

                },
            )

        except Exception as e:
            return response_fun(
                RESPONSE_INVALID,
                {"message": str(e)},
            )