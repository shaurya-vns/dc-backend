 
INTENTS = {

        # ---------------- Product ----------------

        "PRODUCT": [
            "product",
            "products",
            "food",
            "meal",
            "menu",
            "breakfast",
            "lunch",
            "dinner",
            'dishes',
            "veg",
            "offer",
            "offers",
            "discount",
            "cheap",
            "expensive",
            "best food",
            "top rated",
            "popular food"
        ],

         # ---------------- Subscription Order ----------------

       "SUBSCRIPTION_ORDER": [
            "subscription order",
            "my subscription order",

            "today subscription order",
            "subscription today order",

            "subscription breakfast order",
            "subscription lunch order",
            "subscription dinner order",

            "subscription breakfast today order",
            "subscription lunch today order",
            "subscription dinner today order",

            "breakfast subscription order",
            "lunch subscription order",
            "dinner subscription order",
            'subsription order today',

            "today breakfast subscription order",
            "today lunch subscription order",
            "today dinner subscription order",

            "today subscription",
            "today delivery",
            "subscription delivery",
            "track subscription order",
        ],

        # ---------------- One Time Order ----------------

       "ONE_TIME_ORDER": [
            # Specific first
            "show my one time orders",
            "track my today one time order",
            "my one time today order",
            "my today breakfast one time order",
            "my today lunch one time order",
            "my today dinner one time order",
            'my today one time order',
            'latest one time',
            'latest one time order',
            'today one time order',
            # Status
            "pending order",
            "delivered order",
            "cancelled order",
            "completed order",

            # Meal based orders
            "breakfast order",
            "lunch order",
            "dinner order",
        ],

        # ---------------- On Demand ----------------

        "ON_DEMAND_ORDER": [
            "on demand",
            "custom order",
            "special order",
            "vendor price",
            "expected price",
            "approve order",
            "reject order",
            "on demand status"
            'latest on demand',
            'my latest on demand',
            'today on demand',
            'today on demand order'
        ],


        # ---------------- Subscription ----------------

        "SUBSCRIPTION": [
            "subscription",
            "my subscription",
            "active subscription",
            "plan",
            "subscription plan",
            "pause subscription",
            "resume subscription",
            "cancel subscription",
            "subscription status",
            "subscription history",
            "remaining days",
            "expiry",
            "expire"
        ],

       
        # ---------------- Support ----------------

        "HELP_SUPPORT": [
            "help",
            "support",
            "contact",
            "customer care",
            "issue",
            "problem",
            "complaint",
            "refund"
        ]

}

INTENT_PRIORITY = {
    "SUBSCRIPTION_ORDER": 10,
    "SUBSCRIPTION": 5,
}

class IntentDetector:

        @staticmethod
        def detect(message):
            message = message.lower().strip()

            matches = []

            for intent, keywords in INTENTS.items():
                score = 0
                matched_keywords = []

                for keyword in keywords:
                    keyword = keyword.lower()

                    if keyword in message:
                        matched_keywords.append(keyword)

                        # Longer keyword = more importance
                        score += len(keyword)

                if matched_keywords:
                    # Add intent priority
                    score += INTENT_PRIORITY.get(intent, 0)

                    matches.append({
                        "intent": intent,
                        "keywords": matched_keywords,
                        "score": score
                    })

            if matches:

                best_match = max(
                    matches,
                    key=lambda x: x["score"]
                )

                print("keywords:", best_match["keywords"])
                print("intent:", best_match["intent"])

                return best_match["intent"]

            return "UNKNOWN"