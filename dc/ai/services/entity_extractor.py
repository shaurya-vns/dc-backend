from dc.constant import *
from datetime import date, timedelta
import re


class EntityExtractor:

    @staticmethod
    def extract(message):

        entities = {}

        msg = message.lower().strip()


        # --------------------
        # Meal Type
        # --------------------
        meal_types = {
            "breakfast": "BREAKFAST",
            "lunch": "LUNCH",
            "dinner": "DINNER",
        }

        for key, value in meal_types.items():
            if key in msg:
                entities["meal"] = value
                break


        # --------------------
        # Date
        # --------------------
        if "today" in msg:
            entities["date"] = date.today()

        elif "tomorrow" in msg:
            entities["date"] = date.today() + timedelta(days=1)


        # --------------------
        # Offer / Rating
        # --------------------
        if "offer" in msg:
            entities["offer"] = 1

        if "rating" in msg:
            entities["rating"] = 1


        # --------------------
        # Subscription Status
        # --------------------
        subscription_status = {
            "active": ACTIVE,
            "paused": PAUSED,
            "cancelled": CANCELLED,
            "expired": COMPLETED,
        }

        for key, value in subscription_status.items():
            if key in msg:
                entities["subscription_status"] = value
                break


        # --------------------
        # Order Status
        # --------------------
        order_status = {
            "delivered": DELIVERED,
            "preparing": PREPARING,
            "pending": PENDING,
            "cancelled": CANCELLED,
            "skipped": SKIPPED,
        }

        # longest match first
        for key in sorted(order_status, key=len, reverse=True):
            if key in msg:
                entities["status"] = order_status[key]
                break


        # --------------------
        # Latest / Recent
        # --------------------
        if "latest" in msg or "recent" in msg:
            entities["latest"] = True


        # --------------------
        # Best Reviews
        # --------------------
        if any(word in msg for word in [
            "best",
            "top",
            "highest",
            "highest rated",
            "top rated"
        ]):
            entities["rating"] = True


        # --------------------
        # Star Rating
        # --------------------
        star = re.search(r"([1-5])\s*star", msg)

        if star:
            entities["star"] = int(star.group(1))


        return entities