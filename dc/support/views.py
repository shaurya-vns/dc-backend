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
from django.shortcuts import get_object_or_404
  

class SupportViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=CreateSupportTicketSerializer,
        tags=["Raise Issue"],
        manual_parameters=[TOKEN],
    )
    @action(detail=False, methods=["post"])
    def create_update_ticket(self, request):
        try:
            user, error = authenticate_and_get_user(request)

            if error:
                return error

            serializer = CreateSupportTicketSerializer(data=request.data)

            if not serializer.is_valid():
                return response_fun(
                    RESPONSE_INVALID,
                    {"errors": serializer.errors},
                )

            ticket_id = request.data.get("id")

            if ticket_id:
                try:
                    ticket = SupportTicketModel.objects.get(
                        id=ticket_id,
                        user=user
                    )
                except SupportTicketModel.DoesNotExist:
                    return response_fun(
                        RESPONSE_INVALID,
                        {"message": "Ticket not found."},
                    )

                for key, value in serializer.validated_data.items():
                    setattr(ticket, key, value)

                ticket.save()

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Ticket updated successfully.",
                        "ticketId": ticket.id,
                    },
                )

            ticket = SupportTicketModel.objects.create(
                user=user,
                **serializer.validated_data,
            )

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "message": "Ticket created successfully.",
                    "ticketId": ticket.id,
                },
            )

        except Exception as e:
            return response_fun(
                RESPONSE_INVALID,
                {"message": str(e)},
            )
        
    @swagger_auto_schema(
        tags=["Raise Issue"],
        manual_parameters=[
            TOKEN,
            openapi.Parameter(
                "orderId",
                openapi.IN_QUERY,
                description="Order ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    )
    @action(detail=False, methods=["get"])
    def get_ticket_by_order(self, request):
        try:
            user, error = authenticate_and_get_user(request)

            if error:
                return error

            order_id = request.query_params.get("orderId")

            if not order_id:
                return response_fun(
                    RESPONSE_INVALID,
                    {"message": "orderId is required."},
                )

            ticket = (
                SupportTicketModel.objects.filter(
                    user=user,
                    order_id=order_id,
                )
                .order_by("-id")
                .first()
            )

            if not ticket:
                return response_fun(
                    RESPONSE_INVALID,
                    {"message": "No issue found for this order."},
                )

            serializer = SupportTicketDetailSerializer(ticket)

            return response_fun(
                RESPONSE_SUCCESS,
                serializer.data,
            )

        except Exception as e:
            return response_fun(
                RESPONSE_INVALID,
                {"message": str(e)},
            )