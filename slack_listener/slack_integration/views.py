import sys
import os
from loguru import logger
from dotenv import load_dotenv

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .libs.slack_chat_module import SlackPlatform


logger.add(sys.stderr, level="INFO")
logger.add(sys.stderr, level="ERROR")

load_dotenv()


class SlackMessageHandler(APIView):
    def post(self, request):
        SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
        slack_platform = SlackPlatform(SLACK_BOT_TOKEN)
        slack_platform.connect({"token": SLACK_BOT_TOKEN})

        try:
            event_data = request.data
            message = event_data["event"]
            if "text" in message:
                logger.info(f"Received a question from a user {message['user']}: {message['text']}")

                if "thread_ts" not in message or message["ts"] == message["thread_ts"]:
                    channel_id = message["channel"]
                    response_text = "Thanks for your question! We`ll review it and respond shortly."
                    slack_platform.client.chat_postMessage(channel=channel_id,
                                                           text=response_text,
                                                           thread_ts=message["ts"])
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
