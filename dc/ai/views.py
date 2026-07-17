
from rest_framework import viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from dc.utils import response_fun
from dc.constant import RESPONSE_INVALID, RESPONSE_SUCCESS, RESPONSE_ERROR
from dc.errors import  ERROR_CODE_NOT_FOUND
from dc.parameters import TOKEN
from dc.errors import *
from dc.parameters import * 
from dc.utils import authenticate_and_get_user
from ai.serializers import AIChatSerializer, EventStreamRenderer
from ai.services import AIChatService
from django.http import StreamingHttpResponse



class AIViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        tags=["AI"],
        manual_parameters=[TOKEN],
        request_body=AIChatSerializer
    )
    
    @action(
    detail=False,
    methods=["post"],
    renderer_classes=(EventStreamRenderer,)
    )
    def chat_stream(self, request):

        user, error = authenticate_and_get_user(request)

        print('user ', user)


        if error:
            return error
        
        print('user ', user)


        message = request.data.get("message")

        response = StreamingHttpResponse(
            AIChatService.chat_stream(
                user,
                message
            ),
            content_type="text/event-stream"
        )

        response["X-Accel-Buffering"] = "no"
        response["Cache-Control"] = "no-cache, no-transform"


        print(' responseresponse  ', response)

        return response