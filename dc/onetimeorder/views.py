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
from django.db import transaction
from onetimeorder.serializers import OneTimeOrderCreateSerializer
from onetimeorder.serializers import OneTimeOrderDetailSerializer
from dc.constant import *
from address.models import AddressModel 

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

    
                address = AddressModel.objects.filter(
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

                print('delivery_date ', delivery_date)
        
                final_amount =  product.product_price * quantity

                delivery_boy = UserModel.objects.filter(
                        userType=UserModel.DELIVERY,
                        parent=product.vendor,
                        is_active=True
                    ).first()
                

                order = OneTimeOrderModel.objects.create(
                    user=user,
                    product=product,
                    address=address,
                    quantity=quantity,
                    amount=product.product_price,
                    final_amount=final_amount,
                    delivery_date=delivery_date,
                    meal_type=product.plan_type,
                    status= PENDING,
                    delivery  =  delivery_boy
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
                manual_parameters=[TOKEN, DELIVERY_DATE]
        )
        @action(detail=False, methods=["get"])
        def user_one_time_order_list(self, request):
                    try:
                        user, error = authenticate_and_get_user(request)

                        if error:
                            return error
                                         
                        filters = {}

                        filters["user_id"] = request.query_params.get("userId")

                        delivery_date = request.query_params.get("delivery_date")

                        if delivery_date:
                            filters["delivery_date"] = delivery_date
                    
                        
                        orders = OneTimeOrderModel.objects.filter(
                                **filters
                            ).select_related(
                                "product",
                                "offer",
                                "address"
                            ).order_by("delivery_date")


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
            request_body=RejectOneTimeSerializer,
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def vendor_reject(self, request,  pk=None):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                
                order = OneTimeOrderModel.objects.filter(
                    id= pk,
                ).first()

                if order is None:

                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": "Order not found."
                        }
                    )

                order.status = REJECTED
                order.rejectReason = request.data.get("rejectReason")

                order.save()

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Order rejected by vendor"
                    }
                )
            
            
            except Exception as e:
                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": str(e)
                        }
                    )
            
        @swagger_auto_schema(
            tags=["One Time Order"],
            request_body=CancelOneTimeOrderSerializer,
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def user_cancel(self, request,  pk=None):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                
                order = OneTimeOrderModel.objects.filter(
                    id= pk,
                    user = user
                ).first()

                if order is None:

                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": "Order not found."
                        }
                    )

                order.status = CANCELLED
                order.cancelReason = request.data.get("cancelReason")

                order.save()

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Order cancel by user"
                    }
                )
            
            
            except Exception as e:
                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": str(e)
                        }
                    )
            

        @swagger_auto_schema(
            tags=["One Time Order"],
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def vendor_delivery(self, request,  pk=None):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                order = OneTimeOrderModel.objects.filter(
                    id= pk,
                ).first()

                if order is None:

                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": "Order not found."
                        }
                    )
                
                order.status = DELIVERED
                order.save()
                return response_fun(
                            RESPONSE_SUCCESS,
                            {
                                "message": "One time order is delivered."
                            }
                        )
            
            
            except Exception as e:
                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": str(e)
                        }
                    )