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
  

class SubscriptionViewSet(viewsets.ViewSet):
        @swagger_auto_schema(
            tags=["Subscription"],
            request_body=SubscriptionCreateSerializer,
            operation_description="Get next day order",
            responses={200: SubscriptionCreateSerializer, 404: 'Not found'},
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=['post'])
        def create_subscription(self, request):
                try:
                    print('request ', request)
                    customer, error = authenticate_and_get_user(request)
                    print('request customer ', customer)
                    print('request error ', error)

                    if error:
                       return error
                    
                    if customer.userType == CustomerModel.USER_TYPE_CUSTOMER:
                        data = request.data.copy()
                        serializer = SubscriptionCreateSerializer(data=data, context={'request': request,  'customer': customer  })
                        if serializer.is_valid():
                            serializer.save()
                            return response_fun(RESPONSE_SUCCESS, 
                                                {
                                                    'message':"Subscription created successfully",
                                                    'data': serializer.data
                                                }
                                            )
                        return response_fun(RESPONSE_INVALID, {'errors': serializer.errors,'code': ERROR_CODE_BAD_REQUEST}) 
                    return response_fun(RESPONSE_INVALID, {'message': 'Only customer allow','code': ERROR_CODE_NOT_FOUND})
                    

                    
                except Exception as e:
                    print(f'serializer ID {e}')
                    return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
                

        @swagger_auto_schema(
                  tags=["Subscription"],
                  operation_description="Get next day order",
                  responses={200: SubscriptionListSerializer, 404: 'Not found'},
                  manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["get"])
        def my_subscriptions(self, request):

            try:
                print('request ', request)
                customer, error = authenticate_and_get_user(request)
                print('request customer ', customer)
                print('request error ', error)

                if error:
                    return error
                 
                qs = SubscriptionModel.objects.filter(
                    user=customer
                ).order_by("-id")

                serializer = SubscriptionListSerializer(qs, many=True)
                return response_fun(RESPONSE_SUCCESS, 
                                                {
                                                    'message':"Get my subscription list",
                                                    'data': serializer.data
                                                }
                                            )

            except Exception as e:
                 return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
                

            
        @swagger_auto_schema(
                  tags=["Subscription"],
                  operation_description="Get subscription detail by id",
                  responses={200: SubscriptionListSerializer, 404: 'Not found'},
                  manual_parameters=[TOKEN, SUBSCRIPTION_D]
        )
        @action(detail=False, methods=["get"])
        def subscriptions_detail(self, request):

            try:
                print('request ', request)
                customer, error = authenticate_and_get_user(request)
                print('request customer ', customer)
                print('request error ', error)

                if error:
                    return error
                
                subscriptionId = request.GET.get("subscriptionId")
                 
                qs = SubscriptionModel.objects.filter(
                    user=customer,
                    subscription_id=subscriptionId
                )

                serializer = SubscriptionListSerializer(qs)
                return response_fun(RESPONSE_SUCCESS,  {
                                                    'message':"Get my subscription detail",
                                                    'data': serializer.data
                                                })

            except Exception as e:
                 return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
                

            
            