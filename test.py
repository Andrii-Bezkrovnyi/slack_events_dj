import sys
import os

from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter

from loguru import logger
from dotenv import load_dotenv


logger.add(sys.stderr, level="INFO")
logger.add(sys.stderr, level="ERROR")

load_dotenv()


# Получите значения переменных окружения из настроек вашего приложения Slack
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]


# Инициализация WebClient и SlackEventAdapter
client = WebClient(token=SLACK_BOT_TOKEN)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events")

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
    # Запуск сервера прослушивания событий на порту 3000
    slack_events_adapter.start(port=3000, debug=True)