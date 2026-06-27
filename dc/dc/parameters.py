from drf_yasg import openapi

TOKEN=openapi.Parameter('token',openapi.IN_HEADER,type=openapi.TYPE_STRING)

 
ORDER_ID = openapi.Parameter(
    'orderId',
    openapi.IN_QUERY,
    description="Order ID",
    type=openapi.TYPE_INTEGER,
    required=True
)

SUBSCRIPTION_D = openapi.Parameter(
    'subscriptionId',
    openapi.IN_QUERY,
    description="Subscription ID",
    type=openapi.TYPE_INTEGER,
    required=True
)

SUB_OWNER_ID = openapi.Parameter(
    'subOwnerId',
    openapi.IN_QUERY,
    description="Sub Owner ID",
    type=openapi.TYPE_INTEGER,
    required=True
)

USER_ID = openapi.Parameter('userId', openapi.IN_QUERY, description="User ID", type=openapi.TYPE_INTEGER)
