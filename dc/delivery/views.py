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
from order.models import OrderModel
  

class DeliveryViewSet(viewsets.ViewSet):
        @swagger_auto_schema(
            request_body=UpdateOrderStatusSerializer,
            tags=["Delivery"],
            operation_description="update Order specific by orderId, subscriptionId",
            responses={200: UpdateOrderStatusSerializer, 404: 'Not found'},
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["post"])
        def update_order_status(self, request):

            try:
                 
                print('request ', request)
                user, error = authenticate_and_get_user(request)
                print('request user ', user)
                print('request error ', error)
                    
                if error:
                   return error

                serializer = UpdateOrderStatusSerializer(
                    data=request.data
                )

                if not serializer.is_valid():

                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": "Something went wrong !!",
                            "code": ERROR_CODE_NOT_FOUND
                        }
                    )

    
                order = OrderModel.objects.get(
                    id=serializer.validated_data["orderId"],
                    subscription_id=serializer.validated_data["subscriptionId"],
                    user=user
                )

                order.status = serializer.validated_data["status"]
                order.save()

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Order status updated successfully"
                    }
                )

            except OrderModel.DoesNotExist:

                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Order not found",
                        "code": ERROR_CODE_NOT_FOUND
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