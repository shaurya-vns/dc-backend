from django.db.models import Q

from onetimeorder.models import OneTimeOrderModel
import random


class OneTimeOrderHandler:

    @staticmethod
    def execute(user, entities):

        orders = (
            OneTimeOrderModel.objects
            .filter(user=user)
            .select_related(
                "product",
                "offer",
                "address",
                "delivery",
            )
        )

        # --------------------
        # Delivery Date
        # --------------------
        if entities.get("date"):
            orders = orders.filter(
                delivery_date=entities["date"]
            )

        # --------------------
        # Meal Type
        # --------------------
        if entities.get("meal"):
            orders = orders.filter(
                meal_type__contains=entities["meal"].lower()
            )

        # --------------------
        # Order Status
        # --------------------
        if entities.get("status"):
            orders = orders.filter(
                status=entities["status"]
            )

        # --------------------
        # Product Search
        # --------------------
        if entities.get("product"):
            orders = orders.filter(
                product__name__icontains=entities["product"]
            )

        # --------------------
        # Latest Order
        # --------------------
        if entities.get("latest"):
            orders = orders.order_by(
                "-delivery_date",
                "-id"
            )[:1]
        else:
            orders = orders.order_by(
                "-delivery_date",
                "-id"
            )[:10]

        payload = []

        for order in orders:

            item = {

                "id": order.id,

                "order_number": order.order_number,

                "product": order.product.name,

                "delivery_date": str(order.delivery_date),

                "meal_type": order.meal_type,

                "status": order.get_status_display(),

                "quantity": order.quantity,

                "amount": float(order.amount),

                "discount_amount": float(order.discount_amount),

                "final_amount": float(order.final_amount),

            }

            if order.offer:
                item.update({

                    "offer_name": order.offer.name,

                    "offer_discount": float(
                        order.offer.discount_amount
                    )

                })

            payload.append(item)

        if payload:

            intros = [
                "📦 I found your one-time orders!",
                "✨ Your recent meal orders are ready.",
                "🍱 Here are the one-time orders from your account.",
                "👨‍🍳 I found these orders for you.",
            ]

            lines = [
                f"### {random.choice(intros)}",
                "",
                f"I found **{len(payload)} one-time order{'s' if len(payload) > 1 else ''}** for you.",
                f"### 🍛 {item['product']}",
                "",
            ]

            delivered = 0
            pending = 0
            preparing = 0
            cancelled = 0

            for item in payload:

                status = str(item.get("status", "PENDING")).upper()

                if status == "DELIVERED":
                    delivered += 1
                elif status == "PENDING":
                    pending += 1
                elif status == "PREPARING":
                    preparing += 1
                elif status == "CANCELLED":
                    cancelled += 1

            lines.extend([
                "#### 📊 Order Summary",
                "",
            ])

            if delivered:
                lines.append(f"✅ Delivered: **{delivered}**")

            if preparing:
                lines.append(f"👨‍🍳 Preparing: **{preparing}**")

            if pending:
                lines.append(f"⏳ Pending: **{pending}**")

            if cancelled:
                lines.append(f"❌ Cancelled: **{cancelled}**")

            

            return {
                "type": "one_time_order_list",
                "message": "\n".join(lines),
    
            }

        return {

            "type": "empty",

            "message": "No one-time orders found.",

            "payload": []

        }