
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
from django.http import StreamingHttpResponse
import json
import time
from .services.chatbot_service import ChatBotService
from .services.intent_detector import IntentDetector
from .services.entity_extractor import EntityExtractor
from .utils import stream_event, stream_delay



class AIViewSet(viewsets.ViewSet):

        @swagger_auto_schema(
            tags=["AI"],
            manual_parameters=[TOKEN],
            request_body=AIChatSerializer
        )
        @action(
            detail=False,
            methods=["post"]
        )
        def chat_stream(self, request):

            try:
                    user, error = authenticate_and_get_user(request)

                    if error:
                        return error

                    message = request.data.get("message", "").strip()

                    if not message:
                        return response_fun(
                            RESPONSE_INVALID,
                            {
                                "message": 'Message is required.'
                            }
                        )
                        

                    response = ChatBotService.process(
                        user=user,
                        message=message
                    )

                    print('eeeeee response ', response)

                    return response_fun(
                        RESPONSE_SUCCESS,
                        {
                            'data': response,
                        }
                    )
        
            except Exception as e:
                print('sssss ', e)
                return response_fun(
                    RESPONSE_INVALID,
                    {
                        "message": str(e)
                    }
                )
        
 