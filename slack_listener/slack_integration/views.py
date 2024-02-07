from django.views import View
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from slack_sdk import WebClient
from .libs.slack_chat_module import SlackEventHandler, SlackChatPlatform

from dotenv import load_dotenv


load_dotenv()

# class SlackEventView(View):
#     def post(self, request, *args, **kwargs):
#         request_data = json.loads(request.body.decode("utf-8"))
#         SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
#         SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")

#         credentials = {"client": WebClient(token=SLACK_BOT_TOKEN)}
#         slack_chat_platform = SlackChatPlatform(credentials)
#         slack_event_handler = SlackEventHandler(slack_chat_platform)
#         slack_event_handler.handle_message(request_data)
#         return HttpResponse(status=200)


class SlackEventView(APIView):
    def post(self, request, *args, **kwargs):
        SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
        SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
        credentials = {"client": WebClient(token=SLACK_BOT_TOKEN)}
        slack_chat_platform = SlackChatPlatform(credentials)
        slack_event_handler = SlackEventHandler(slack_chat_platform)
        slack_event_handler.handle_message(request.data)
        return Response(status=status.HTTP_200_OK)