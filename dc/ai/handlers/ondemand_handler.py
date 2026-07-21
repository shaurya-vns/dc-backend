from ondemand.models import OnDemandModel
import random

class OnDemandHandler:

    @staticmethod
    def execute(user, entities):

        orders = OnDemandModel.objects.filter(
            user=user
        ).select_related(
            "vendor",
            "delivery",
            "address"
        )

        # -----------------------
        # Delivery Date
        # -----------------------

        if entities.get("date"):
            orders = orders.filter(
                deliveryDate=entities["date"]
            )

        # -----------------------
        # Meal Type
        # -----------------------

        if entities.get("meal"):
            orders = orders.filter(
                meal_type__contains=entities["meal"].lower()
            )

        # -----------------------
        # Status
        # -----------------------

        if entities.get("status"):
            orders = orders.filter(
                status=entities["status"]
            )

        # -----------------------
        # Latest Order
        # -----------------------

        if entities.get("latest"):
            orders = orders.order_by(
                "-deliveryDate",
                "-id"
            )[:1]

        else:
            orders = orders.order_by(
                "-deliveryDate",
                "-id"
            )[:10]

        payload = []

        for order in orders:

            payload.append({
                "id": order.id,
                "order_number": order.orderNumber,
                "item_name": order.itemName,
                "meal_type": order.get_mealType_display(),
                "quantity": order.quantity,
                "delivery_date": str(order.deliveryDate),
                "status": order.get_status_display(),
                "vendorAmount": float(order.vendorAmount),
                "vendor": order.vendor.name if order.vendor else None,
                "delivery_partner": order.delivery.name if order.delivery else None,
                "image": order.image.url if order.image else None,
                "cancelReason": order.cancelReason,
                "rejectReason": order.rejectReason,
                "note": order.note,
            })


        if payload:

            import random

            intros = [
                "🍱 I found your custom meal orders!",
                "✨ Your on-demand orders are ready.",
                "👨‍🍳 Here are your special meal requests.",
                "📦 I found your custom food orders.",
            ]

            lines = [
                f"### {random.choice(intros)}",
                "",
                f"I found **{len(payload)} on-demand order{'s' if len(payload) > 1 else ''}** for you.",
                "",
            ]


            for item in payload:

                status = item["status"].upper()

                if status == "APPROVED":
                    note = "✅ Approved by vendor."
                elif status in ["PENDING", "WAITING"]:
                    note = "⏳ Waiting for confirmation."
                elif status == "REJECTED":
                    note = "❌ Order request was rejected."
                elif status == "CANCELLED":
                    note = "🚫 Order was cancelled."
                else:
                    note = "🍽️ Order status updated."


                lines.extend([
                    f"### 🍛 {item['item_name']}",
                    f"`{status}`",
                    "",
                    note,
                    "",
                ])

            return {
                "type": "ondemand_order_list",
                "message": "\n".join(lines),
                "payload": payload
            }
        return {

            "type": "empty",

            "message": "No on-demand orders found.",

            "payload": []

        }