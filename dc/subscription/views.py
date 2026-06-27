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
from .service import SubscriptionService
  

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
                    user, error = authenticate_and_get_user(request)
                    print('request user ', user)
                    print('request error ', error)

                    if error:
                       return error
                    
                    # ONLY CUSTOMER ALLOWED
                    if user.userType != UserModel.USER:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "Only customer allowed",
                                "code": ERROR_CODE_NOT_FOUND
                            }
                        )
                    
                    serializer = SubscriptionCreateSerializer(
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
                    parent =  user.parent
                    print('user parent ', parent)
                    print('proudct owner ', product.subOwner)

                    if product.subOwner_id != user.parent_id:
                        return  response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": 'Invalid access: product does not belong to your SubOwner.',
                                "code": ERROR_CODE_BAD_REQUEST
                            } 
                         )

                    subscription = SubscriptionService.create_subscription(
                        user = user,
                        product = data["product"],
                        pricing_options=data["pricing_options"],
                        start_date=data["start_date"],
                    )

                    return response_fun(RESPONSE_SUCCESS,{
                            "message": "Subscription created successfully",
                            "data": {
                                "id": subscription.id,
                                "userId": subscription.user.id,
                                "subOwnerId": subscription.subOwner.id,
                                "productId": subscription.product.id,
                                "pricingId": subscription.pricing_options.id,
                                "start_date": subscription.start_date,
                                "end_date": subscription.end_date,
                                "status": subscription.status,
                            }
                        }
                    )
                    
                except Exception as e:
                    print('error ', e)
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
                user, error = authenticate_and_get_user(request)
                print('request user ', user)
                print('request error ', error)

                if error:
                    return error
                 
                qs = SubscriptionModel.objects.filter(
                    user=user
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
                user, error = authenticate_and_get_user(request)
                print('request customer ', user)
                print('request error ', error)

                if error:
                    return error
                
                subscriptionId = request.GET.get("subscriptionId")
                 
                qs = SubscriptionModel.objects.filter(
                    user=user,
                    subscription_id=subscriptionId
                )

                serializer = SubscriptionListSerializer(qs)
                return response_fun(RESPONSE_SUCCESS,  {
                                                    'message':"Get my subscription detail",
                                                    'data': serializer.data
                                                })

            except Exception as e:
                 return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
                

            
            
        @swagger_auto_schema(
                  tags=["Subscription"],
                  operation_description="Pause subscription",
                  manual_parameters=[TOKEN, SUBSCRIPTION_D]
        )
        @action(detail=False, methods=["get"])
        def subscriptions_pause(self, request):

            try:
                print('request ', request)
                user, error = authenticate_and_get_user(request)
                print('request user ', user)
                print('request error ', error)

                if error:
                    return error
                
                subscriptionId = request.GET.get("subscriptionId")
                 
                subscription = SubscriptionModel.objects.get(
                        id=subscriptionId,
                        user=user
                    )
                
                subscription.status = "paused"
                subscription.save()

                OrderModel.objects.filter(subscription=subscription,
                        status="pending"
                    ).update(
                        status="paused"
                    )

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Subscription paused successfully"
                    } )
            
            except Exception as e:
                 return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
                

            
        @swagger_auto_schema(
                  tags=["Subscription"],
                  operation_description="Cancelled subscription",
                  manual_parameters=[TOKEN, SUBSCRIPTION_D]
        )
        @action(detail=False, methods=["get"])
        def subscriptions_cancelled(self, request):

            try:
                print('request ', request)
                user, error = authenticate_and_get_user(request)
                print('request customer ', user)
                print('request error ', error)

                if error:
                    return error
                
                subscriptionId = request.GET.get("subscriptionId")
                 
                subscription = SubscriptionModel.objects.get(
                        id=subscriptionId,
                        user=user
                    )
                
                subscription.status = "cancelled"
                subscription.save()

                OrderModel.objects.filter(
                        subscription=subscription,
                        status__in=["pending", "paused"]
                    ).update(
                        status="cancelled"
                    )

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Subscription cancelled successfully"
                    } )
            
            except Exception as e:
                 return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
                

            
        @swagger_auto_schema(
                  tags=["Subscription"],
                  operation_description="Resume subscription",
                  manual_parameters=[TOKEN, SUBSCRIPTION_D]
        )
        @action(detail=False, methods=["get"])
        def subscriptions_resume(self, request):

            try:
                print('request ', request)
                user, error = authenticate_and_get_user(request)
                print('request user ', user)
                print('request error ', error)

                if error:
                    return error
                
                subscriptionId = request.GET.get("subscriptionId")
                 
                subscription = SubscriptionModel.objects.get(
                        id=subscriptionId,
                        user=user
                    )
                
                subscription.status = "active"
                subscription.save()

                OrderModel.objects.filter(
                    subscription=subscription,
                    status="paused"
                ).update(
                    status="pending"
                )

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Subscription resumed successfully"
                    } )
            
            except Exception as e:
                 return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
                

            
       