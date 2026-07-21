from django.db.models import Q

from product.models import ProductModel
import random

class ProductHandler:

    @staticmethod
    def execute(user, entities):

        products = ProductModel.objects.filter(
            is_active=True
        )

        # ------------------------
        # Search by name/title
        # ------------------------

        if entities.get("search"):
            keyword = entities["search"]

            products = products.filter(
                Q(name__icontains=keyword) |
                Q(title__icontains=keyword)
            )

        # ------------------------
        # Meal Type
        # ------------------------

        if entities.get("meal"):
            meal = entities["meal"].lower()
            products = products.filter(
                plan_type__contains = meal
            )

        # ------------------------
        # Plan Type
        # ------------------------

        if entities.get("plan"):
            plan = entities["plan"].lower()
            products = products.filter(
                plan_type__contains= plan
            )

        # ------------------------
        # Category
        # ------------------------

        if entities.get("category"):
            category = entities["category"].lower()

            products = products.filter(
                category__icontains=category
            )

        # ------------------------
        # Offer Products
        # ------------------------

        if entities.get("offer"):
            products = products.filter(
                offer__isnull=False,
                offer__is_active=True
            )

        # ------------------------
        # Price
        # ------------------------

        if entities.get("min_price"):
            products = products.filter(
                product_price__gte=entities["min_price"]
            )

        if entities.get("max_price"):
            products = products.filter(
                product_price__lte=entities["max_price"]
            )

        # ------------------------
        # Sort
        # ------------------------

        if entities.get("rating"):

            products = products.order_by("-rating")

        elif entities.get("price_low"):

            products = products.order_by("product_price")

        elif entities.get("price_high"):

            products = products.order_by("-product_price")

        elif entities.get("latest"):

            products = products.order_by("-created_at")

        else:

            products = products.order_by("-created_at")

        # ------------------------
        # Limit
        # ------------------------

        
        limit = entities.get("limit", 5)
        products = products[:limit]

        payload = []

        for product in products:
            payload.append({
                "name": product.name,
                "title": product.title,
                "price": float(product.product_price),
                "rating": float(product.rating),
                "image": product.images[0] if product.images else None,
                "offer_name": product.offer.name if product.offer else None,
                "offer_discount": float(product.offer.discount_amount) if product.offer else None,
            })

        if payload:

            intros = [
                "🍽️ I found some delicious meals for you!",
                "✨ Here are a few meal options you might enjoy!",
                "👨‍🍳 Great choice! I found these meals for you.",
                "🎉 These meals match your request.",
            ]

            lines = [
                f"### {random.choice(intros)}",
                "",
                f"I found **{len(payload)}** meal{'s' if len(payload) > 1 else ''} matching your request.",
                "",
            ]

            for item in payload:

                descriptions = []

                # Rating
                if item["rating"] >= 4.8:
                    descriptions.append("🌟 Highly rated by customers.")
                elif item["rating"] >= 4.5:
                    descriptions.append("⭐ Popular choice with great reviews.")

                # Price
                if item["price"] <= 120:
                    descriptions.append("💰 Budget-friendly option.")
                elif item["price"] >= 250:
                    descriptions.append("👑 Premium meal experience.")

                # Offer
                if item["offer_name"]:
                    descriptions.append(
                        f"🎁 Save **₹{int(item['offer_discount'])}** with the **{item['offer_name']}** offer."
                    )

                # Default
                if not descriptions:
                    descriptions.append("🍽️ Freshly prepared and worth trying.")

                lines.extend([
                    f"### 🍛 {item['name']}",
                    f"**{item['title']}**",
                    "",
                    " ".join(descriptions),
                    "",
                ])


            return {
                "type": "product_list",
                "message": "\n".join(lines),
            }

        return {

            "type": "empty",

            "message": "No products found matching your request.",

            "payload": []

        }