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
from .service import SubscriptionService
from dc.constant import *
 

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
                    isApplyOffer = data["isApplyOffer"]
                    address_id = data["addressId"]

                    subscription_exists = SubscriptionModel.objects.filter(
                        product_id=product.id,
                        user = user
                    ).exists()

                    if subscription_exists:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "User has already subscription",
                                "code": ERROR_CODE_NOT_FOUND
                            }
                        )


                     
                    address = AddressModel.objects.filter(
                            id=address_id,
                            user=user
                        ).first()
                    
                    if not address:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": 'Inavlid address id',
                                "code": ERROR_CODE_BAD_REQUEST
                            }
                        )

                    subscription = SubscriptionService.create_subscription(
                        user = user,
                        product = product,
                        address = address,
                        pricing_options=data["pricing_options"],
                        start_date=data["start_date"],
                        quantity=data["quantity"],
                        isApplyOffer=isApplyOffer,
                    )

                    return response_fun(RESPONSE_SUCCESS,{
                            "message": "Subscription created successfully",
                            "data": {
                                "orderNumber": subscription.sub_number
                           }
                        }
                    )
                    
                except Exception as e:
                    print('error ', e)
                    return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !! , ','code': ERROR_CODE_NOT_FOUND}) 
                
        @swagger_auto_schema(
            tags=["Subscription"],
            operation_description="Genrate Subscription order when payment done",
            responses={200: SubscriptionCreateSerializer, 404: 'Not found'},
            manual_parameters=[TOKEN, SUBSCRIPTION_D]
        )
        @action(detail=False, methods=['get'])
        def subscription_approve_payment(self, request):
                try:
                    print('request ', request)
                    user, error = authenticate_and_get_user(request)
                    print('request user ', user)
                    print('request error ', error)

                    if error:
                       return error
                    
                    # ONLY CUSTOMER ALLOWED
                    if user.userType != UserModel.SUB_OWNER:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "Only admin can approve subscription payment.",
                                "code": ERROR_CODE_NOT_FOUND
                            }
                        )
                    
                    subscriptionId = request.GET.get("subscriptionId")

                    order_exists = OrderModel.objects.filter(
                        subscription_id=subscriptionId
                    ).exists()

                    if order_exists:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "Order already created for this subscription",
                                "code": ERROR_CODE_NOT_FOUND
                            }
                        )

                    subscription = SubscriptionModel.objects.get(
                        id = subscriptionId
                    )

                    if subscription.status == ACTIVE:
                         return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "Subscription already active",
                                "code": ERROR_CODE_NOT_FOUND
                            }
                        )
                    
                    SubscriptionService.generate_orders(
                        user = subscription.user,
                        subscription = subscription
                     )

                    return response_fun(RESPONSE_SUCCESS,{
                            "message": "Payment approved successfully",
                            "data": {
                                 "orderNumber": subscription.sub_number,
                    
                            }
                        }
                    )
                    
                except Exception as e:
                    print('error ', e)
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
            


        @swagger_auto_schema(
                  tags=["SubOwner"],
                  operation_description="Subscrioption list by user ID",
                  responses={200: SubscriptionListSerializer, 404: 'Not found'},
                  manual_parameters=[TOKEN, USER_ID]
        )
        @action(detail=False, methods=["get"])
        def subscriptions_list_by_user_id(self, request):

                try:
        
                    user, error = authenticate_and_get_user(request)
                    
                    if error:
                        return error
                    
                    user_id = request.query_params.get("userId")
            
                    filters = {}

                    if user_id:
                            filters["user_id"] = user_id

                    subscriptions = SubscriptionModel.objects.filter(
                        **filters
                    ).order_by("-id")
                    
                    serializer = SubscriptionListSerializer(subscriptions, many=True)
                    return response_fun(RESPONSE_SUCCESS, 
                                                    {
                                                        'message':"Subscrioption list",
                                                        'data': serializer.data
                                                    }
                                                )

                except Exception as e:
                    return response_fun(RESPONSE_INVALID, {'message': 'Something went  wrong !!','code': ERROR_CODE_NOT_FOUND}) 
                    
                

            
       