from rest_framework import viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .serializers import *
from dc.utils import response_fun
from dc.constant import RESPONSE_INVALID, RESPONSE_SUCCESS
from dc.errors import   ERROR_CODE_NOT_FOUND
from dc.parameters import TOKEN
from dc.utils import authenticate_and_get_user
from dc.errors import *
from dc.parameters import *
from order.serializers import OrderListSerializer
from owner.serializers import UpdateOrderStatusSerializer

from dc.constant import *
  

class OrderViewSet(viewsets.ViewSet):
         
        @swagger_auto_schema(
            tags=["Subscription Order"],
            operation_description="Get today order",
            responses={200: OrderListSerializer, 404: 'Not found'},
            manual_parameters=[TOKEN, USER_ID, DELIVERY_DATE]
        )
        @action(detail=False, methods=["get"])
        def subscription_user_order_list(self, request):

            try:
                print('request ', request)
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
                        "user_id": user_id
                    }

                    # ✅ OPTIONAL DATE FILTER
                if delivery_date:
                        filters["delivery_date"] = delivery_date

                orders = OrderModel.objects.filter(
                     **filters
                ).order_by("-delivery_date")

                print('request orders ', orders)

                serializer = OrderListSerializer(
                    orders,
                    many=True
                )

                return response_fun(RESPONSE_SUCCESS,
                                    {
                                          'message':"Subscription Today's orders",
                                          'data': serializer.data
                                    })

            except Exception as e:
                return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
            

        @swagger_auto_schema(
                    request_body=UpdateOrderStatusSerializer,
                    tags=["Subscription Order"],
                    operation_description="Update order status",
                    responses={200: UpdateOrderStatusSerializer},
                    manual_parameters=[TOKEN, ORDER_ID]
                )
        @action(detail=False, methods=["put"])
        def update_sub_order_status(self, request):
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

                        order = OrderModel.objects.filter( id=order_id).first()

                        if not order:
                            return response_fun(
                                RESPONSE_INVALID,
                                {
                                    "message": "Order not found.",
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
                                "message": "Order status updated successfully."
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

                