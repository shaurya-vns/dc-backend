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
    tags=["Support"],
    manual_parameters=[TOKEN]
    )
    @action(detail=False, methods=["post"])
    def create_ticket(self, request):

        user, error = authenticate_and_get_user(request)

        if error:
            return error

        ticket = SupportTicketModel.objects.create(

            user=user,

            subOwner_id=request.data.get("subOwner"),

            subscription_order_id=request.data.get(
                "subscription_order"
            ),

            one_time_order_id=request.data.get(
                "one_time_order"
            ),

            subject=request.data.get("subject"),

            issue_type=request.data.get("issue_type"),
        )

        SupportMessageModel.objects.create(

            ticket=ticket,

            sender=user,

            message=request.data.get("message"),
        )

        serializer = SupportTicketDetailSerializer(ticket)

        return response_fun(
            RESPONSE_SUCCESS,
            {
                "message": "Support ticket created.",
                "data": serializer.data,
            },
        )
    
    @swagger_auto_schema(
        tags=["Support"],
        manual_parameters=[TOKEN]
    )
    @action(detail=False, methods=["get"])
    def my_tickets(self, request):

        user, error = authenticate_and_get_user(request)

        if error:
            return error

        qs = SupportTicketModel.objects.filter(
            user=user
        ).order_by("-created_at")

        serializer = SupportTicketSerializer(
            qs,
            many=True
        )

        return response_fun(
            RESPONSE_SUCCESS,
            {
                "data": serializer.data
            }
        )
                

    @swagger_auto_schema(
        tags=["Support"],
        manual_parameters=[TOKEN]
    )
    @action(detail=True, methods=["get"])
    def ticket_detail(self, request, pk=None):

        user, error = authenticate_and_get_user(request)

        if error:
            return error

        ticket = get_object_or_404(

            SupportTicketModel,

            id=pk,

            user=user
        )

        serializer = SupportTicketDetailSerializer(ticket)

        return response_fun(
            RESPONSE_SUCCESS,
            {
                "data": serializer.data
            }
        )
    
    @swagger_auto_schema(
        tags=["Support"],
        manual_parameters=[TOKEN]
    )
    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):

        user, error = authenticate_and_get_user(request)

        if error:
            return error

        ticket = get_object_or_404(

            SupportTicketModel,

            id=pk
        )

        msg = SupportMessageModel.objects.create(

            ticket=ticket,

            sender=user,

            message=request.data.get("message"),

            image=request.FILES.get("image"),
        )

        serializer = SupportMessageSerializer(msg)

        return response_fun(
            RESPONSE_SUCCESS,
            {
                "message": "Message sent.",
                "data": serializer.data,
            },
        )
    
    @swagger_auto_schema(
        tags=["Support"],
        manual_parameters=[TOKEN]
    )
    @action(detail=True, methods=["put"])
    def close_ticket(self, request, pk=None):

        user, error = authenticate_and_get_user(request)

        if error:
            return error

        ticket = get_object_or_404(

            SupportTicketModel,

            id=pk,

            user=user
        )

        ticket.status = SupportTicketModel.CLOSED

        ticket.save()

        return response_fun(
            RESPONSE_SUCCESS,
            {
                "message": "Ticket closed."
            }
        )
    
    @swagger_auto_schema(
        tags=["Support"],
        operation_description="Get ticket messages",
        manual_parameters=[TOKEN]
    )
    @action(detail=True, methods=["get"])
    def ticket_messages(self, request, pk=None):
        try:
            user, error = authenticate_and_get_user(request)

            if error:
                return error

            ticket = SupportTicketModel.objects.filter(
                id=pk
            ).first()

            if ticket is None:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Support ticket not found.",
                        "code": ERROR_CODE_NOT_FOUND
                    }
                )

            # Customer can only view their own tickets
            if user.userType == UserModel.USER and ticket.user_id != user.id:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Permission denied.",
                        "code": RESPONSE_INVALID
                    }
                )

            # Sub Owner can only view tickets assigned to them
            if user.userType == UserModel.SUB_OWNER and ticket.subOwner_id != user.id:
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": "Permission denied.",
                        "code": RESPONSE_INVALID
                    }
                )

            messages = SupportMessageModel.objects.filter(
                ticket=ticket
            ).select_related(
                "sender"
            ).order_by("created_at")

            serializer = SupportMessageSerializer(
                messages,
                many=True
            )

            return response_fun(
                RESPONSE_SUCCESS,
                {
                    "message": "Ticket messages",
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