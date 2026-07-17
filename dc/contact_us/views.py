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
  

class ContactUsViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        tags=["Contact Us"],
        request_body=CreateContactUsSerializer,
        manual_parameters=[TOKEN],
    )
    @action(detail=False, methods=["post"])
    def user_create(self, request):
        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error

            serializer = CreateContactUsSerializer(data=request.data)

            if not serializer.is_valid():
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "errors": serializer.errors
                    }
                )

            ticket = ContactUsModel.objects.create(
                user=user,
                name=serializer.validated_data["name"],
                phoneNumber=serializer.validated_data["phoneNumber"],
                subject=serializer.validated_data["subject"],
                message=serializer.validated_data["message"]
            )

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "message": "Your contact us successfuly added.",
                    "id": ticket.id,
                },
            )

        except Exception as e:
            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": str(e)
                }
            )
        
    @swagger_auto_schema(
        tags=["Contact Us"],
        manual_parameters=[TOKEN],
    )
    @action(detail=False, methods=["get"])
    def user_request_list(self, request):
        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error

            queryset = ContactUsModel.objects.filter(
                user=user
            )

            serializer = ContactUsSerializer(queryset, many=True)

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    'data': serializer.data,
                }
            )

        except Exception as e:
            print('sssss ', e)
            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": str(e)
                }
            )
        
    @swagger_auto_schema(
        tags=["Contact Us"],
        manual_parameters=[TOKEN, CONTACT_US_ID],
    )
    @action(detail=False, methods=["get"])
    def user_detail(self, request):
        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error

            obj = ContactUsModel.objects.filter(
                id=request.query_params.get("id"),
                user=user,
            ).first()

            if obj is None:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Request not found."
                    }
                )

            serializer = ContactUsSerializer(obj)

            return response_fun(
                RESPONSE_SUCCESS,
                serializer.data,
            )

        except Exception as e:
            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": str(e)
                }
            )
        
    @swagger_auto_schema(
        tags=["Contact Us"],
        manual_parameters=[TOKEN],
    )
    @action(detail=False, methods=["get"])
    def admin_list(self, request):
        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error

            queryset = ContactUsModel.objects.select_related(
                "user"
            ).order_by("-createdAt")

            serializer = ContactUsSerializer(queryset, many=True)

            return response_fun(
                RESPONSE_SUCCESS,
                serializer.data,
            )

        except Exception as e:
            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": str(e)
                }
            )
        
    @swagger_auto_schema(
        tags=["Contact Us"],
        request_body=UpdateContactStatusSerializer,
        manual_parameters=[TOKEN],
    )
    @action(detail=True, methods=["put"])
    def admin_update_status(self, request, pk=None):
        try:

            user, error = authenticate_and_get_user(request)

            if error:
                return error

            serializer = UpdateContactStatusSerializer(data=request.data)

            if not serializer.is_valid():
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "errors": serializer.errors
                    }
                )

            obj = ContactUsModel.objects.filter(id=pk).first()

            if obj is None:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Request not found."
                    }
                )

            obj.status = serializer.validated_data["status"]
            obj.adminRemark = serializer.validated_data.get(
                "adminRemark",
                ""
            )

            obj.save(update_fields=[
                "status",
                "adminRemark",
            ])

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "message": "Status updated successfully."
                },
            )

        except Exception as e:
            return response_fun(
                RESPONSE_INVALID,
                {
                    "message": str(e)
                }
            )