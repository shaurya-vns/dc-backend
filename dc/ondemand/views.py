 
 
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
from rest_framework import viewsets
from rest_framework.decorators import action 
from ondemand.serializers import UpdateOnDemandSerializer
from dc.constant import *
 
class OnDemandViewSet(viewsets.ViewSet):
        
        @swagger_auto_schema(
            tags=["On Demand"],
            request_body=OnDemandCreateSerializer,
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["post"])
        def create(self, request):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                

                print('req date ', request.data)

                serializer = OnDemandCreateSerializer(
                    data=request.data,
                    context={"user": user}
                )

                serializer.is_valid(raise_exception=True)

                serializer.save()

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "On demand order created successfully."
                    }
                )

            except Exception as e:
                print('eeee e ', e)
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": str(e),
                        "code": ERROR_CODE_NOT_FOUND
                    }
                )
            
        @swagger_auto_schema(
            tags=["On Demand"],
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["get"])
        def on_demand_list(self, request):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                filters = {}

                filters["user_id"] = request.query_params.get("userId")
                
                orders = OnDemandModel.objects.filter(
                          **filters
                    ).select_related(
                        "address",
                        "vendor"
                    ).order_by("-created_at")
                     

                serializer = OnDemandSerializer(
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

                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": str(e)
                    }
                )
        

        @swagger_auto_schema(
            tags=["On Demand"],
            request_body=CancelUserDemandSerializer,
            manual_parameters=[TOKEN],
        )
        @action(detail=False, methods=["put"])
        def user_cancel(self, request, pk=None):
            try:
                user, error = authenticate_and_get_user(request)

                if error:
                    return error

                serializer = CancelUserDemandSerializer(data=request.data)

                if not serializer.is_valid():
                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": "Cancel reason is required."
                        },
                    )
                            
                order = OnDemandModel.objects.filter(
                    id=pk,
                    user=user,
                ).first()

                if order is None:
                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": "Order not found."
                        },
                    )

                if order.status == CANCELLED:
                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": "Order is already cancelled."
                        },
                    )

                order.status = CANCELLED
                order.cancelReason = serializer.validated_data["cancelReason"]
                order.save(update_fields=["status", "cancelReason"])

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Order cancelled successfully by user."
                    },
                )

            except Exception as e:
                print('eee ', e)
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": str(e)
                    },
                )
    

        @swagger_auto_schema(
            tags=["On Demand"],
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def user_approve(self, request, pk=None):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                print('order id ', pk)

                order = OnDemandModel.objects.filter(
                    id=pk,
                    user=user
                ).first()

                if order is None:

                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": "Order not found."
                        }
                    )
                
                # When vendor set vendor amount and user move to approved
                if order.status == WAITING:
                    order.finalAmount = order.vendorAmount
                    order.status = APPROVED
                    order.save()
                    return response_fun(
                    RESPONSE_SUCCESS,
                            {
                                "message": "Order approved by user."
                            }
                        )
                
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "User can only when vendor amount added"
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
            tags=["On Demand"],
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def vendor_approve(self, request,  pk=None):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                

                order = OnDemandModel.objects.filter(
                    id= pk,
                  
                ).first()

                if order is None:

                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": "Order not found."
                        }
                    )

                order.finalAmount = order.userAmount
                order.vendorAmount = order.userAmount
                order.status = APPROVED

                order.save()

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Order approved by vendor"
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
            tags=["On Demand"],
            request_body=RejectUserDemandSerializer,
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def vendor_reject(self, request,  pk=None):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                
                order = OnDemandModel.objects.filter(
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
            tags=["On Demand"],
            request_body=UpdateOnDemandSerializer,
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def vendor_update_amount(self, request,  pk=None):
            try:

                    user, error = authenticate_and_get_user(request)

                    if error:
                        return error
                    

                    
                    order = OnDemandModel.objects.filter(
                        id= pk,
                         
                    ).first()

                    if order is None:

                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": "Order not found."
                            }
                        )
                    
                    vendorAmount = request.data.get("vendorAmount")

                    order.vendorAmount = vendorAmount

                    order.status = WAITING

                    order.save()

                    return response_fun(
                        RESPONSE_SUCCESS,
                        {
                            "message": "Vendor update vendor amount."
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
            tags=["On Demand"],
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def vendor_approve_payment(self, request,  pk=None):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                 
                
                order = OnDemandModel.objects.filter(
                    id= pk,
                  
                ).first()

                if order is None:

                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": "Order not found."
                        }
                    )
                
                if order.status ==  APPROVED:
                    order.status = PAID
                    order.save()
                    return response_fun(
                            RESPONSE_SUCCESS,
                            {
                                "message": "Payment successfully done."
                            }
                        )

                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "invalid data."
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
            tags=["On Demand"],
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["put"])
        def vendor_delivery(self, request,  pk=None):

            try:

                user, error = authenticate_and_get_user(request)

                if error:
                    return error
                
                order = OnDemandModel.objects.filter(
                    id= pk,
                    
                ).first()

                if order is None:

                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": "Order not found."
                        }
                    )
                
                if order.status ==  PAID:
                    order.status = DELIVERED
                    order.save()
                    return response_fun(
                            RESPONSE_SUCCESS,
                            {
                                "message": "On demand order is delivered."
                            }
                        )

                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "invalid data."
                    }
                )
            
            
            except Exception as e:
                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": str(e)
                        }
                    )