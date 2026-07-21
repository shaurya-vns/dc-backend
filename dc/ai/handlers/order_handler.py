from django.db.models import Q

from order.models import OrderModel
import random

class OrderHandler:

    @staticmethod
    def execute(user, entities):

        orders = OrderModel.objects.filter(
            user=user
        ).select_related(
            "subscription",
            "subscription__product"
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

            payload.append({

                "product": order.subscription.product.name,

                "delivery_date": str(order.delivery_date),

                "meal_type": order.get_meal_type_display(),

                "status": order.get_status_display(),

                "amount": float(order.subscription.amount),

            })

        if payload:



            intros = [
                "📦 I found your meal orders!",
                "🍱 Here are your recent meal deliveries.",
                "✨ Your order details are ready.",
                "👨‍🍳 I found these orders for you.",
            ]

            lines = [
                f"### {random.choice(intros)}",
                "",
                f"I found **{len(payload)} order{'s' if len(payload) > 1 else ''}** in your account.",
                "",
            ]

            status_summary = {}

            for item in payload:

                status = item.get("status", "PENDING").upper()
                meal_type = item.get("meal_type", "Meal")

                status_summary[status] = status_summary.get(status, 0) + 1

                if status == "DELIVERED":
                    status_icon = "✅ Delivered"
                    description = "Your meal has been delivered successfully."
                
                elif status == "PREPARING":
                    status_icon = "👨‍🍳 Preparing"
                    description = "Your meal is being prepared by the kitchen."
                
                elif status == "PENDING":
                    status_icon = "⏳ Pending"
                    description = "Your order is waiting for confirmation."
                
                elif status == "CANCELLED":
                    status_icon = "❌ Cancelled"
                    description = "This order has been cancelled."
                
                elif status == "SKIPPED":
                    status_icon = "⏭️ Skipped"
                    description = "This meal delivery was skipped."
                
                else:
                    status_icon = "📌 " + str(status)
                    description = "Your order status has been updated."

                lines.extend([
                    f"### 🍱 {meal_type}",
                    f"`{status_icon}`",
                    "",
                    f"📅 **Delivery Date:** {item.get('delivery_date')}",
                    f"🔢 **Quantity:** {item.get('quantity', 1)}",
                    "",
                    description,
                    "",
                ])

            if status_summary:

                lines.extend([
                    "---",
                    "",
                    "### 📊 Order Summary",
                    "",
                ])

                for status, count in status_summary.items():
                    lines.append(
                        f"• {status}: **{count}**"
                    )

                lines.append("")

            return {
                "type": "order_list",
                "message": "\n".join(lines),
            }
        return {

            "type": "empty",

            "message": "No orders found.",

            "payload": []

        }