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
    # Get environment variable values from your Slack app settings
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
    SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
    target_channel_id = os.getenv("TARGET_CHANNEL_ID")

    # Create an instance of a class for Slack
    slack_factory = SlackPlatform(SLACK_BOT_TOKEN)

    # Connect to Slack
    slack_factory.connect({"token": SLACK_BOT_TOKEN})
    app = App(token=SLACK_BOT_TOKEN)

    # Initializing WebClient
    client = WebClient(token=SLACK_BOT_TOKEN)

    # Initializing SlackEventAdapter
    slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events")

    # Initializing Bolt app
    app = App(token=SLACK_BOT_TOKEN)

    # Handling the "message" event (new message)
    @slack_events_adapter.on("message")
    def handle_message(event_data):
        message = event_data["event"]

        if "text" in message:
            logger.info(f"Received a question from a user {message['user']}: {message['text']}")

            # Checking if the message is the last one in the thread
            if "thread_ts" not in message or message["ts"] == message["thread_ts"]:
                channel_id = message["channel"]
                response_text = "Thanks for your question! We`ll review it and respond shortly."
                client.chat_postMessage(channel=channel_id, text=response_text, thread_ts=message["ts"])

    if __name__ == "__main__":
        slack_events_adapter.start(port=8000, debug=True)
