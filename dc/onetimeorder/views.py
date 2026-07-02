from rest_framework import viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .serializers import *
from dc.utils import response_fun
from dc.constant import RESPONSE_INVALID, RESPONSE_SUCCESS
from dc.errors import   ERROR_CODE_NOT_FOUND
from django.contrib.auth.hashers        import make_password
from dc.parameters import TOKEN
from dc.utils import authenticate_and_get_user
from dc.errors import *
from dc.parameters import *
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.db import transaction
  
from onetimeorder.serializers import OneTimeOrderCreateSerializer
from onetimeorder.serializers import OneTimeOrderDetailSerializer


class OneTimeOrderViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        tags=["One Time Order"],
        request_body=OneTimeOrderCreateSerializer,
        manual_parameters=[TOKEN]
    )
    @action(detail=False, methods=["post"])
    @transaction.atomic
    def create_order(self, request):
        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error

            if user.userType != UserModel.USER:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Only customer allowed",
                        "code": ERROR_CODE_BAD_REQUEST
                    }
                )

            serializer = OneTimeOrderCreateSerializer(
                data=request.data,
                context={"user": user}
            )

            if not serializer.is_valid():
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": serializer.errors,
                        "code": ERROR_CODE_BAD_REQUEST
                    }
                )

            data = serializer.validated_data

            product = data["product"]

            # Product belongs to customer's SubOwner
            if product.subOwner_id != user.parent_id:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Invalid product.",
                        "code": ERROR_CODE_BAD_REQUEST
                    }
                )

            # Address validation
            address = UserAddress.objects.filter(
                id=data["addressId"],
                user=user
            ).first()

            if not address:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Invalid address.",
                        "code": ERROR_CODE_BAD_REQUEST
                    }
                )

            quantity = data["quantity"]

            # ------------------------------------
            # Calculate price from Product Pricing
            # ------------------------------------

            pricing = product.pricing_options.order_by("days").first()

            if not pricing:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Pricing not available.",
                        "code": ERROR_CODE_BAD_REQUEST
                    }
                )

            per_day_price = (
                Decimal(pricing.price) /
                Decimal(pricing.days)
            )

            amount = per_day_price * quantity

            # ------------------------------------
            # Offer
            # ------------------------------------

            discount = Decimal("0.00")
            offer = None

            if data["isApplyOffer"]:

                offer = product.offer

                if (
                    offer
                    and offer.is_active
                    and offer.start_date <= timezone.now() <= offer.end_date
                ):
                    discount = offer.discount_amount

            final_amount = max(
                amount - discount,
                Decimal("0.00")
            )

            order = OneTimeOrderModel.objects.create(
                user=user,
                subOwner=product.subOwner,
                product=product,
                address=address,
                quantity=quantity,
                amount=amount,
                discount_amount=discount,
                final_amount=final_amount,
                offer=offer,
                delivery_date=timezone.localdate(),
                meal_type=product.plan_type,
                status=OneTimeOrderModel.PENDING,
            )

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "message": "Order placed successfully.",
                    "data": {
                        "id": order.id,
                        "amount": order.amount,
                        "discount": order.discount_amount,
                        "final_amount": order.final_amount,
                        "status": order.status
                    }
                }
            )

        except Exception as e:
            print(e)

            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": str(e),
                    "code": ERROR_CODE_BAD_REQUEST
                }
            )
        
    @swagger_auto_schema(
        tags=["One Time Order"],
        operation_description="My One-Time Orders",
        manual_parameters=[TOKEN]
    )
    @action(detail=False, methods=["get"])
    def my_orders(self, request):
        try:
            user, error = authenticate_and_get_user(request)

            if error:
                return error

            orders = OneTimeOrderModel.objects.filter(
                user=user
            ).select_related(
                "product",
                "offer",
                "address"
            ).order_by("-created_at")

            serializer = OneTimeOrderDetailSerializer(
                orders,
                many=True
            )

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "data": serializer.data
                }
            )

        except Exception as e:
            print(e)
            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": str(e),
                    "code": ERROR_CODE_BAD_REQUEST
                }
            )
        
    @swagger_auto_schema(
        tags=["One Time Order"],
        operation_description="Order Detail",
        manual_parameters=[TOKEN, PRODUCT_ORDER_ID]
    )
    @action(detail=False, methods=["get"])
    def order_detail(self, request):

        try:
            user, error = authenticate_and_get_user(request)

            if error:
                return error

            order_id = request.GET.get("orderId")

            order = OneTimeOrderModel.objects.select_related(
                "product",
                "offer",
                "address"
            ).filter(
                id=order_id,
                user=user
            ).first()

            if not order:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Order not found",
                        "code": ERROR_CODE_NOT_FOUND
                    }
                )

            serializer = OneTimeOrderDetailSerializer(order)

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "data": serializer.data
                }
            )

        except Exception as e:
            print(e)

            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": str(e),
                    "code": ERROR_CODE_BAD_REQUEST
                }
            )
        
    @swagger_auto_schema(
        tags=["One Time Order"],
        operation_description="Today's Orders",
        manual_parameters=[TOKEN]
    )
    @action(detail=False, methods=["get"])
    def today_orders(self, request):

        try:
            user, error = authenticate_and_get_user(request)

            if error:
                return error

            today = timezone.localdate()

            orders = OneTimeOrderModel.objects.filter(
                user=user,
                delivery_date=today
            ).select_related(
                "product",
                "offer",
                "address"
            ).order_by("created_at")

            serializer = OneTimeOrderDetailSerializer(
                orders,
                many=True
            )

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "data": serializer.data
                }
            )

        except Exception as e:
            print(e)

            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": str(e),
                    "code": ERROR_CODE_BAD_REQUEST
                }
            )