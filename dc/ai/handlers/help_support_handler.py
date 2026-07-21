class HelpSupportHandler:
       
    @staticmethod
    def execute(user, entities):

        return {
            "type": "text",
            "message": (
                "🤝 **Customer Support**\n\n"
                "Need help with your order, subscription, payment, or delivery?\n\n"
                "📞 **Phone:** +91 XXXXX XXXXX\n"
                "📧 **Email:** support@example.com\n\n"
                "Our support team will be happy to assist you."
            )
        }