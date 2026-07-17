from rest_framework import renderers
from rest_framework import serializers
 

class AIChatSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)

class EventStreamRenderer(renderers.BaseRenderer):
    media_type = "text/event-stream"
    format = "event-stream"
    charset = "utf-8"