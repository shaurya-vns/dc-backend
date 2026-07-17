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
from dc.constant import *
  

class OrderViewSet(viewsets.ViewSet):
         
        @swagger_auto_schema(
            tags=["Subscription Order"],
            operation_description="Get today order",
            responses={200: OrderListSerializer, 404: 'Not found'},
            manual_parameters=[TOKEN, DELIVERY_DATE]
        )
        @action(detail=False, methods=["get"])
        def subscription_user_order_list(self, request):

            try:
                print('request ', request)
                user, error = authenticate_and_get_user(request)
                
                    
                if error:
                   return error
                
                filters = {}

                filters["user_id"] = request.query_params.get("userId")
                 
                delivery_date = request.query_params.get("delivery_date")

                if delivery_date:
                        filters["delivery_date"] = delivery_date

                orders = OrderModel.objects.filter(
                     **filters
                ).order_by("delivery_date")

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
            tags=["Subscription Order"],
            request_body=RejectOrderSerializer,
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def vendor_reject(self, request,  pk=None):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                
                order = OrderModel.objects.filter(
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
            tags=["Subscription Order"],
            request_body=CancelOrderSerializer,
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def user_cancel(self, request,  pk=None):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                
                order = OrderModel.objects.filter(
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
            tags=["Subscription Order"],
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def vendor_delivery(self, request,  pk=None):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                order = OrderModel.objects.filter(
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
                                "message": "On demand order is delivered."
                            }
                        )
            
            
            except Exception as e:
                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": str(e)
                        }
                    )