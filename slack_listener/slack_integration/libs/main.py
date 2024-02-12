import sys
import os

from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter

from loguru import logger
from dotenv import load_dotenv

from slack_bolt import App

from .slack_chat_module import SlackPlatform

logger.add(sys.stderr, level="INFO")
logger.add(sys.stderr, level="ERROR")


load_dotenv()


if __name__ == "__main__":
    # Получите значения переменных окружения из настроек вашего приложения Slack
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
    SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
    target_channel_id = os.getenv("TARGET_CHANNEL_ID")

    # Create an instance of a class for Slack
    slack_factory = SlackPlatform(SLACK_BOT_TOKEN)

    # Connect to Slack
    slack_factory.connect({"token": SLACK_BOT_TOKEN})
    app = App(token=SLACK_BOT_TOKEN)

    # Инициализация WebClient
    client = WebClient(token=SLACK_BOT_TOKEN)

    # Инициализация SlackEventAdapter
    slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events")

    # Instantiate the Bolt app
    app = App(token=SLACK_BOT_TOKEN)

    # Обработка события "message" (нового сообщения)
    @slack_events_adapter.on("message")
    def handle_message(event_data):
        message = event_data["event"]

        if "text" in message:
            logger.info(f"Received a question from a user {message['user']}: {message['text']}")

            # Проверяем, является ли сообщение последним в треде
            if "thread_ts" not in message or message["ts"] == message["thread_ts"]:
                channel_id = message["channel"]
                response_text = "Thanks for your question! We`ll review it and respond shortly."
                client.chat_postMessage(channel=channel_id, text=response_text, thread_ts=message["ts"])

    if __name__ == "__main__":
        slack_events_adapter.start(port=8000, debug=True)
