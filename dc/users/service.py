from datetime import timedelta
from django.db import transaction

from subscription.models import SubscriptionModel
from order.models import OrderModel
from users.models import UserModel
from product.models import ProductModel, ProductPricingModel
from subscription.service import SubscriptionService
from users.helper import create_subscription_orders


class UserService:

    @staticmethod
    @transaction.atomic
    def change_subowner(user, data):

        subscription = SubscriptionModel.objects.select_for_update().get(
            id=data["subscriptionId"],
            user=user,
            status = SubscriptionModel.ACTIVE
        )

        new_sub_owner = UserModel.objects.get(
            id=data["newSubOwnerId"],
            userType=UserModel.SUB_OWNER,
            is_active=True,
        )

        product = ProductModel.objects.get(
            id=data["newProductId"],
            subOwner=new_sub_owner,
            is_active=True,
        )

        pricing = ProductPricingModel.objects.get(
            id=data["newPricingOptionId"],
            product=product,
        )

        print('subscription ', subscription)
        print('new_sub_owner ', new_sub_owner)
        print('product ', product)
        print('pricing ', pricing)

        total_days = pricing.days

        #
        # 1. Close old subscription
        #
        subscription.status = SubscriptionModel.TRANSFERRED
        subscription.end_date = data["startDate"] - timedelta(days=1)
        subscription.save()

        #
        # 2. Cancel future orders
        #
        OrderModel.objects.filter(
            subscription=subscription,
            status=OrderModel.PENDING,
            delivery_date__gte=data["startDate"],
        ).update(
            status=OrderModel.CANCELLED
        )

        #
        # 3. Create new subscription
        #
        new_subscription = SubscriptionModel.objects.create(
            user=user,
            subOwner=new_sub_owner,
            product=product,
            pricing_options=pricing,
            start_date=data["startDate"],
            end_date=data["startDate"] + timedelta(days=pricing.days - 1),
            total_days=pricing.days,
            amount=pricing.price,
            status=SubscriptionModel.ACTIVE,
        )

        print('22222')

        #
        # 4. Generate Orders
        #
        create_subscription_orders(new_subscription)

        return new_subscription
    