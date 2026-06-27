from rest_framework import viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from .models import *
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
from subscription.models import SubscriptionModel
from order.serializers import OrderListSerializer
from support.serializers import UpdateSupportRequestSerializer
from support.models import SupportRequestModel
from users.models import UserModel
from users.serializers import SubOwnerListSerializer
  

class DashboardViewSet(viewsets.ViewSet):
        @swagger_auto_schema(
            tags=["Dashboard"],
            operation_description="Get dashboard",
            manual_parameters=[TOKEN]
        )
        @action(detail=False, methods=["get"])
        def get_dashboard(self, request):

            try:
                 
                print('request ', request)
                user, error = authenticate_and_get_user(request)
                print('request user ', user)
                print('request error ', error)
                    
                if error:
                   return error

                today = timezone.now().date()
                tomorrow = today + timedelta(days=1)

                active_subscriptions = SubscriptionModel.objects.filter(
                    user=user,
                    status="active"
                ).count()

                today_orders = OrderModel.objects.filter(
                    user=user,
                    delivery_date=today
                ).count()

                tomorrow_orders = OrderModel.objects.filter(
                    user=user,
                    delivery_date=tomorrow
                ).count()

                pending_orders = OrderModel.objects.filter(
                    user=user,
                    status="pending"
                ).count()

                delivered_orders = OrderModel.objects.filter(
                    user=user,
                    status="delivered"
                ).count()

                upcoming_delivery = OrderModel.objects.filter(
                    user=user,
                    delivery_date__gte=today
                ).order_by(
                    "delivery_date"
                ).first()

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Dashboard data fetched successfully",
                        "data": {
                            "activeSubscriptions": active_subscriptions,
                            "todayOrders": today_orders,
                            "tomorrowOrders": tomorrow_orders,
                            "pendingOrders": pending_orders,
                            "deliveredOrders": delivered_orders,
                            "nextDeliveryDate": (
                                upcoming_delivery.delivery_date
                                if upcoming_delivery else None
                            )
                        }
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
            tags=["Dashboard"]
        )
        @action(detail=False, methods=["get"])
        def today_orders(self, request):

            try:

                today = timezone.now().date()

                orders = OrderModel.objects.filter(
                    delivery_date=today
                ).select_related(
                    "customer",
                    "subscription",
                    "subscription__product"
                ).order_by(
                    "meal_type"
                )

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Today's orders fetched successfully",
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
            
        @swagger_auto_schema(
            tags=["Dashboard"],
            operation_description="Get all Sub owner list",
        )
        @action(detail=False, methods=["get"])
        def get_subowner_list(self, request):

            try:

                sub_owners = UserModel.objects.filter(
                    userType=UserModel.SUB_OWNER,
                    is_active=True
                ).order_by("-id")

                serializer = SubOwnerListSerializer(sub_owners, many=True)

                return response_fun(
                    RESPONSE_SUCCESS,
                    {
                        "message": "Sub owner list",
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