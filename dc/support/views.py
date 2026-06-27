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
  

class SupportViewSet(viewsets.ViewSet):
        @swagger_auto_schema(
            tags=["Support"],
            request_body=CreateSupportRequestSerializer,
            operation_description="Request support",
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["post"])
        def create_request(self, request):

            try:

                print('request ', request)
                customer, error = authenticate_and_get_user(request)
               
                if error:
                       return error

                serializer = CreateSupportRequestSerializer(data=request.data)

                if not serializer.is_valid():

                    return response_fun(
                        RESPONSE_INVALID,
                        {
                            "message": serializer.errors
                        }
                    )


                order = OrderModel.objects.get(
                    id=serializer.validated_data["orderId"],
                    customer=customer
                )

                support = SupportRequestModel.objects.create(
                    customer=customer,
                    order=order,
                    subscription=order.subscription,
                    request_type=serializer.validated_data["request_type"],
                    subject=serializer.validated_data["subject"],
                    message=serializer.validated_data["message"]
                )

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Request submitted successfully",
                        "requestId": support.id
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
            tags=["Support"],
            operation_description="Request support",
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["get"])
        def my_requests(self, request):
            try:
                print('request ', request)
                customer, error = authenticate_and_get_user(request)
               
                if error:
                       return error

                requests = SupportRequestModel.objects.filter(customer=customer
                ).order_by("-id")

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "data": SupportRequestListSerializer(
                            requests,
                            many=True
                        ).data
                    }
                )

            except Exception as e:

                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": str(e)
                    }
                )
            
            

            