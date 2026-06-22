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
  

class OrderViewSet(viewsets.ViewSet):
        @swagger_auto_schema(
            tags=["Order"],
            operation_description="Get My Order List",
            responses={200: OrderListSerializer, 404: 'Not found'},
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=['get'])
        def my_orders(self, request):
                try:
                    print('request ', request)
                    customer, error = authenticate_and_get_user(request)
                    print('request customer ', customer)
                    
                    if error:
                       return error
                    
                    qs = OrderModel.objects.filter(customer=customer).order_by("-id")

                    serializer = OrderListSerializer(qs, many=True)
                    return response_fun(RESPONSE_SUCCESS,{
                                                 'message':"Subscription created successfully",
                                                   'data': serializer.data
                                                  })
    
                except Exception as e:
                    print(f'serializer ID {e}')
                    return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
                

        @swagger_auto_schema(
            tags=["Order"],
            operation_description="Get Order Detail specific by ID",
            responses={200: OrderListSerializer, 404: 'Not found'},
            manual_parameters=[TOKEN, ORDER_ID, SUBSCRIPTION_D]
        )
        @action(detail=False, methods=["get"])
        def order_detail(self, request):

            try:
                
                print('request ', request)
                customer, error = authenticate_and_get_user(request)
                print('request customer ', customer)
                print('request error ', error)
                    
                if error:
                   return error

                orderId = request.GET.get("orderId")
                subscriptionId = request.GET.get("subscriptionId")
                print('request orderId ', orderId)


                order = OrderModel.objects.filter(
                    customer=customer,
                    id=orderId,
                    subscription_id=subscriptionId
                ).order_by(
                    "delivery_date",
                    "meal_type"
                )

                serializer = OrderListSerializer(order)

                return response_fun(RESPONSE_SUCCESS,
                                    {
                                          'message':"Order detail",
                                          'data': serializer.data
                                    })
            except Exception as e:
                return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
            
        @swagger_auto_schema(
            tags=["Order"],
            operation_description="Get upcoming order",
            responses={200: OrderListSerializer, 404: 'Not found'},
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["get"])
        def upcoming_orders(self, request):

            try:

                print('request ', request)
                customer, error = authenticate_and_get_user(request)
                print('request customer ', customer)
                print('request error ', error)
                    
                if error:
                   return error

                orders = OrderModel.objects.filter(
                    customer=customer,
                    delivery_date__gte=timezone.now().date()
                ).order_by(
                    "delivery_date"
                )

                serializer = OrderListSerializer(
                    orders,
                    many=True
                )

                return response_fun(RESPONSE_SUCCESS,
                                    {
                                          'message':"Upcoming orders",
                                          'data': serializer.data
                                    })

            except Exception as e:
                return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
            
        @swagger_auto_schema(
            tags=["Order"],
            operation_description="Get today order",
            responses={200: OrderListSerializer, 404: 'Not found'},
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["get"])
        def today_orders(self, request):

            try:
                print('request ', request)
                customer, error = authenticate_and_get_user(request)
                print('request customer ', customer)
                print('request error ', error)
                    
                if error:
                   return error

                today = timezone.now().date()
                print('request today ', today)

                orders = OrderModel.objects.filter(
                    customer=customer,
                    delivery_date=today
                )

                print('request orders ', orders)

                serializer = OrderListSerializer(
                    orders,
                    many=True
                )

                return response_fun(RESPONSE_SUCCESS,
                                    {
                                          'message':"Today's orders",
                                          'data': serializer.data
                                    })

                

            except Exception as e:
                return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
            

        @swagger_auto_schema(
            tags=["Order"],
            operation_description="Get next day skip order",
            responses={200: OrderListSerializer, 404: 'Not found'},
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["get"])
        def next_day_orders(self, request):

            try:

                print('request ', request)
                customer, error = authenticate_and_get_user(request)
                print('request customer ', customer)
                print('request error ', error)
                    
                if error:
                   return error

                next_date = timezone.now().date() + timedelta(days=1)

                orders = OrderModel.objects.filter(
                    customer=customer,
                    delivery_date=next_date
                ).order_by("meal_type")

                serializer = OrderListSerializer(
                    orders,
                    many=True
                )

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Next day orders fetched successfully",
                        "data": serializer.data
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
            
        @swagger_auto_schema(
            tags=["Order"],
            operation_description="Get Order Detail specific by ID",
            responses={200: OrderListSerializer, 404: 'Not found'},
            manual_parameters=[TOKEN, SUBSCRIPTION_D]
        )
        @action(detail=False, methods=["get"])
        def get_order_by_subscription_id(self, request):

            try:
                
                print('request ', request)
                customer, error = authenticate_and_get_user(request)
                print('request customer ', customer)
                print('request error ', error)
                    
                if error:
                   return error

                subscriptionId = request.GET.get("subscriptionId")
                print('request subscriptionId ', subscriptionId)

                orders = OrderModel.objects.filter(
                    customer=customer,
                    subscription_id=subscriptionId
                ).order_by(
                    "delivery_date",
                    "meal_type"
                )

                print('request order ', orders)

                serializer = OrderListSerializer(orders,   many=True)

                return response_fun(RESPONSE_SUCCESS,
                                    {
                                          'message':"Subscription created successfully",
                                          'data': serializer.data
                                    })
            except Exception as e:
                return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
            
        
        @swagger_auto_schema(
            tags=["Order"],
            operation_description="Get Order history",
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["get"])
        def order_history(self, request):

            try:

                print('request ', request)
                customer, error = authenticate_and_get_user(request)
                print('request customer ', customer)
                print('request error ', error)
                    
                if error:
                   return error

                orders = OrderModel.objects.filter(
                    customer=customer,
                    status__in=[
                        "delivered",
                        "cancelled",
                        "skipped"
                    ]
                ).select_related(
                    "subscription",
                    "subscription__product"
                ).order_by(
                    "-delivery_date"
                )

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Order history fetched successfully",
                        "data": OrderListSerializer(
                            orders,
                            many=True
                        ).data
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