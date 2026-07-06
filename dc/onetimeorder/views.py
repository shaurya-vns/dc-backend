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
from owner.serializers import UpdateOrderStatusSerializer
  
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
            delivery_date = data["delivery_date"]
    
            final_amount =  product.product_price * quantity

            order = OneTimeOrderModel.objects.create(
                user=user,
                subOwner=product.subOwner,
                product=product,
                address=address,
                quantity=quantity,
                amount=product.product_price,
                final_amount=final_amount,
                delivery_date=delivery_date,
                meal_type=product.plan_type,
                status=OneTimeOrderModel.PENDING,
            )

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "message": "Order placed successfully.",
                    "data": {
                        "id": order.id,
                        "orderNumber": order.order_number,
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
            operation_description="Get User all One-Time Orders",
            manual_parameters=[TOKEN, USER_ID, DELIVERY_DATE]
    )
    @action(detail=False, methods=["get"])
    def user_one_time_order_list(self, request):
                try:
                    user, error = authenticate_and_get_user(request)

                    if error:
                        return error
                    
            
                    user_id = request.query_params.get("userId")
                    delivery_date = request.query_params.get("delivery_date")

                    if not user_id:
                        return response_fun(
                            RESPONSE_INVALID,
                            {"message": "user_id is required"},
                        )
                    

                    filters = {
                        "user_id": user_id,
                        "status": OneTimeOrderModel.PENDING,
                    }

                    # ✅ OPTIONAL DATE FILTER
                    if delivery_date:
                        filters["delivery_date"] = delivery_date
                    else:
                        # default = today
                        filters["delivery_date"] = timezone.localdate()

                    
                    orders = OneTimeOrderModel.objects.filter(
                            **filters
                        ).select_related(
                            "product",
                            "offer",
                            "address"
                        ).order_by("-delivery_date")


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
                request_body=UpdateOrderStatusSerializer,
                tags=["One Time Order"],
                operation_description="Update one time order status",
                responses={200: UpdateOrderStatusSerializer},
                manual_parameters=[TOKEN, ORDER_ID]
            )
    @action(detail=False, methods=["put"])
    def update_onetime_order_status(self, request):
                try:
                    user, error = authenticate_and_get_user(request)

                    if error:
                        return error
                    
                    if user.userType != UserModel.SUB_OWNER:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "Only sub owner is aloowed!.",
                                "code": ERROR_CODE_BAD_REQUEST
                            }
                        )

                    order_id = request.query_params.get("orderId")

                    if not order_id:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "orderId is required.",
                                "code": ERROR_CODE_BAD_REQUEST
                            }
                        )

                    order = OneTimeOrderModel.objects.filter(id=order_id).first()

                    if not order:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "One time Order not found.",
                                "code": ERROR_CODE_NOT_FOUND
                            }
                        )

                    serializer = UpdateOrderStatusSerializer(data=request.data)

                    if not serializer.is_valid():
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "errors": serializer.errors,
                                "code": ERROR_CODE_BAD_REQUEST
                            }
                        )

                    order.status = serializer.validated_data["status"]
                    order.save(update_fields=["status"])

                    return response_fun(
                        RESPONSE_SUCCESS,
                        {
                            "message": "One time Order status updated successfully."
                        }
                    )

                except Exception as e:
                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": str(e),
                            "code": ERROR_CODE_NOT_FOUND
                        }
                    )
          