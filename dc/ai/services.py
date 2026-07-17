from django.conf import settings
from groq import Groq

from .prompts import tiffin_ai_prompt
from .utils import (
    get_product_context,
    get_order_context,
    get_subscription_context,
    get_one_time_order_context,
    get_ondemand_order_context
)


client = Groq(
    api_key=settings.GROQ_API_KEY
)


class AIChatService:


    @staticmethod
    def chat_stream(user, message):

        products = get_product_context()

        subscription_orders = get_order_context(user)

        subscriptions = get_subscription_context(user)

        one_time_orders = get_one_time_order_context(user)

        on_demand_orders = get_ondemand_order_context(user)


        prompt = tiffin_ai_prompt(

            user,

            products,

            subscription_orders,

            subscriptions,

            one_time_orders,

            on_demand_orders,

            message

        )


        stream = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                "role": "system",
                "content":
                """
                You are a Tiffin App AI assistant.
                Always answer in clean Markdown format.
                """
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.3,

            max_completion_tokens=1024,

            stream=True
        )

        for chunk in stream:

            content = chunk.choices[0].delta.content


            if content:

                yield f"data: {content}\n\n"