 
 
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

            review = ReviewService.create_review(user, serializer.validated_data)

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "message": "Review submitted successfully.",
                    "data": {
                        "id": review.id,
                        "rating": review.rating,
                        "review": review.review,
                    },
                },
            )

        except OrderModel.DoesNotExist:

            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": "Delivered order not found.",
                    "code": ERROR_CODE_NOT_FOUND,
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
    @action(detail=False, methods=["get"], url_path="product_reviews")
    def product_reviews(self, request):

        product_id = request.query_params.get("productId")

        if not product_id:
            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": "productId is required",
                    "code": ERROR_CODE_BAD_REQUEST,
                },
            )

        try:
            product = ProductModel.objects.get(
                id=product_id,
                is_active=True
            )
        except ProductModel.DoesNotExist:
            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": "Product not found",
                    "code": ERROR_CODE_NOT_FOUND,
                },
            )

        reviews = ReviewModel.objects.filter(
            product=product
        ).select_related(
            "user",
            "subOwner"
        ).order_by("-createdAt")

        avg_rating = reviews.aggregate(
            avg=Avg("rating"),
            total=Count("id")
        )

        serializer = ProductReviewSerializer(
            reviews,
            many=True
        )

        return response_fun(
            RESPONSE_SUCCESS,
            {
                "productId": product.id,
                "productName": product.name,
                "averageRating": round(avg_rating["avg"] or 0, 1),
                "totalReviews": avg_rating["total"],
                "reviews": serializer.data,
            },
        )
    
    @swagger_auto_schema(
        tags=["Reviews"],
        manual_parameters=[TOKEN, SUB_OWNER_ID],
    )
    @action(detail=False, methods=["get"], url_path="subowner_reviews")
    def subowner_reviews(self, request):

        sub_owner_id = request.query_params.get("subOwnerId")

        if not sub_owner_id:
            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": "subOwnerId is required",
                    "code": ERROR_CODE_BAD_REQUEST,
                },
            )

        try:
            sub_owner = UserModel.objects.get(
                id=sub_owner_id,
                userType=UserModel.SUB_OWNER,
                is_active=True
            )
        except UserModel.DoesNotExist:
            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": "SubOwner not found",
                    "code": ERROR_CODE_NOT_FOUND,
                },
            )

        reviews = ReviewModel.objects.filter(
            subOwner=sub_owner
        ).select_related(
            "user",
            "product",
            "order"
        ).order_by("-createdAt")

        agg = reviews.aggregate(
            averageRating=Avg("rating"),
            totalReviews=Count("id")
        )

        serializer = ProductReviewSerializer(
            reviews,
            many=True
        )

        return response_fun(
            RESPONSE_SUCCESS,
            {
                "subOwnerId": sub_owner.id,
                "subOwnerName": sub_owner.name,
                "averageRating": round(agg["averageRating"] or 0, 1),
                "totalReviews": agg["totalReviews"],
                "reviews": serializer.data,
            },
        )