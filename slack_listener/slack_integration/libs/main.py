import os
import sys

from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter

from loguru import logger
from dotenv import load_dotenv

from slack_chat_module import SlackChatPlatform, SlackEventHandler


logger.add(sys.stderr, level="INFO")
logger.add(sys.stderr, level="ERROR")

load_dotenv()


if __name__ == "__main__":

    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")

    credentials = {"client": WebClient(token=SLACK_BOT_TOKEN)}
    slack_chat_platform = SlackChatPlatform(credentials)
    slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events")
    slack_event_handler = SlackEventHandler(slack_chat_platform)

    @slack_events_adapter.on("message")
    def handle_message(event_data):
        slack_event_handler.handle_message(event_data)

    slack_events_adapter.start(port=3000, debug=True)
