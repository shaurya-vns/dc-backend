from .intent_detector import IntentDetector
from .entity_extractor import EntityExtractor

from ..handlers.product_handler import ProductHandler
from ..handlers.subscription_handler import SubscriptionHandler
from ..handlers.order_handler import OrderHandler
from ..handlers.one_time_order_handler import OneTimeOrderHandler
from ..handlers.ondemand_handler import OnDemandHandler
from ..handlers.help_support_handler import HelpSupportHandler


HANDLERS = {

    "PRODUCT": ProductHandler,

    "SUBSCRIPTION": SubscriptionHandler,

    "SUBSCRIPTION_ORDER": OrderHandler,

    "ONE_TIME_ORDER": OneTimeOrderHandler,

    "ON_DEMAND_ORDER": OnDemandHandler,

    "HELP_SUPPORT": HelpSupportHandler,

}


class ChatBotService:

    @staticmethod
    def process(user, message):

        print('message  ', message)

        intent = IntentDetector.detect(message)

        entities = EntityExtractor.extract(message)

        print('intent  ', intent)
        print('entities  ', entities)

        handler = HANDLERS.get(
            intent,
            HelpSupportHandler
        )

        print('handler  ', handler)

        return handler.execute(
            user,
            entities
        )