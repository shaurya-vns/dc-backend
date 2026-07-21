from datetime import date

from subscription.models import SubscriptionModel
from dc.constant import *

import random

class SubscriptionHandler:

    @staticmethod
    def execute(user, entities):

        subscriptions = SubscriptionModel.objects.filter(
            user=user
        ).select_related(
            "product",
            "pricing_options",
            "address"
        )

        # -----------------------
        # Status
        # -----------------------

        if entities.get("subscription_status"):
            subscriptions = subscriptions.filter(
                status=entities["subscription_status"]
            )

        else:
            subscriptions = subscriptions.filter(
                status=ACTIVE
            )

        # -----------------------
        # Date Filter
        # -----------------------

        if entities.get("date"):

            subscriptions = subscriptions.filter(
                start_date__lte=entities["date"],
                end_date__gte=entities["date"]
            )

        # -----------------------
        # Product Search
        # -----------------------

        if entities.get("search"):

            subscriptions = subscriptions.filter(
                product__name__icontains=entities["search"]
            )

        # -----------------------
        # Meal Type
        # -----------------------

        if entities.get("meal"):

            subscriptions = subscriptions.filter(
                product__meal_type=entities["meal"]
            )

        # -----------------------
        # Latest Subscription
        # -----------------------

        if entities.get("latest"):

            subscriptions = subscriptions.order_by(
                "-created_at"
            )[:1]

        else:

            subscriptions = subscriptions.order_by(
                "-created_at"
            )

        payload = []

        today = date.today()

        for sub in subscriptions:

            remaining_days = max(
                (sub.end_date - today).days,
                0
            )

            payload.append({

                "subscription_number": sub.sub_number,

                "product": sub.product.name,

                "quantity": sub.quantity,

                "start_date": str(sub.start_date),

                "end_date": str(sub.end_date),

                "remaining_days": remaining_days,

                "payment_status": sub.get_payment_status_display(),

                "status": sub.get_status_display(),

                "amount": float(sub.amount),

                "discount_amount": float(sub.discount_amount),

                "original_price": float(sub.original_price),

            })

        if payload:

    

            intros = [
                "📦 I found your active subscriptions!",
                "✨ Here are your subscription details.",
                "🍱 Your meal subscriptions are ready.",
                "👨‍🍳 I found these subscription plans for you.",
            ]

            lines = [
                f"### {random.choice(intros)}",
                "",
                f"I found **{len(payload)} subscription{'s' if len(payload) > 1 else ''}** linked to your account.",
                "",
            ]

            active_count = 0
            paused_count = 0
            completed_count = 0

            for item in payload:

                status = item.get("status")
                print('status ', status)

                if status == 'Active':
                    active_count += 1
                    tag = "🟢 Active"
                elif status == 'Paused':
                    paused_count += 1
                    tag = "⏸️ Paused"
                elif status == 'Completed':
                    completed_count += 1
                    tag = "✅ Completed"
                else:
                    tag = "📌 Subscription"

                lines.extend([
                    f"#### 🍱 {item.get('product')}",
                    f"`{tag}`",
                    "",
                    f"📅 **Duration:** {item.get('start_date')} → {item.get('end_date')}",
                    f"💰 **Amount:** ₹{item.get('amount')}",
                    "",
                ])

            summary = []

            if active_count:
                summary.append(f"🟢 {active_count} active")

            if paused_count:
                summary.append(f"⏸️ {paused_count} paused")

            if completed_count:
                summary.append(f"✅ {completed_count} completed")

            if summary:
                lines.extend([
                    "",
                    "#### 📊 Subscription Summary",
                    "",
                    " • ".join(summary),
                    "",
                ])
        

            return {
                "type": "subscription_list",
                "message": "\n".join(lines),
            }

        return {

            "type": "empty",

            "message": "No subscriptions found.",

            "payload": []

        }