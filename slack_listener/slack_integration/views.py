from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from libs.slack_chat_module import SlackEventHandler, SlackChatPlatform

import os
import sys

from slack_sdk import WebClient
from loguru import logger
from dotenv import load_dotenv

logger.add(sys.stderr, level="INFO")
logger.add(sys.stderr, level="ERROR")

load_dotenv()

class SlackEventView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body.decode("utf-8"))
        SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
        SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")

        credentials = {"client": WebClient(token=SLACK_BOT_TOKEN)}
        slack_chat_platform = SlackChatPlatform(credentials)
        slack_event_handler = SlackEventHandler(slack_chat_platform)
        slack_event_handler.handle_message(request_data)
        return HttpResponse(status=200)

