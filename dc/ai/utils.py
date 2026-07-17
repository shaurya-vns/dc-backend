import re
from product.models import ProductModel
from order.models import OrderModel
from subscription.models import SubscriptionModel
from onetimeorder.models import OneTimeOrderModel
from ondemand.models import OnDemandModel


def clean_ai_response(text):

    if not text:
        return ""


    # Remove Qwen/Reasoning tags if any
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL
    )


    return text.strip()

@staticmethod
def get_product_context():

        return list(
            ProductModel.objects.filter(
                is_active=True
            )
            .values(
                "id",
                "name",
                "title",
                "category",
                "product_price",
                "description"
            )[:20]
        )



@staticmethod
def get_order_context(user):

        return list(
            OrderModel.objects.filter(
                user=user
            )
            .order_by("-id")
            .values(
                "id",
                "meal_type",
                "status",
                "delivery_date"
            )[:5]
        )



@staticmethod
def get_one_time_order_context(user):

        return list(
            OneTimeOrderModel.objects.filter(
                user=user
            )
            .order_by("-id")
            .values(
                "id",
                "status",
                "meal_type",
                "delivery_date"
            )[:5]
        )



@staticmethod
def get_ondemand_order_context(user):

        return list(
            OnDemandModel.objects.filter(
                user=user
            )
            .order_by("-id")
            .values(
                "id",
                "itemName",
                "deliveryDate",
                "address"
            )[:5]
        )



@staticmethod
def get_subscription_context(user):

        return list(
            SubscriptionModel.objects.filter(
                user=user
            )
            .order_by("-id")
            .values(
                "id",
                "status",
                "start_date",
                "end_date"
            )[:5]
        )
