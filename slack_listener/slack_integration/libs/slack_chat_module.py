import requests
from loguru import logger

from interfaces import ChatPlatform, Conversation, Message


logger.add("app.log", level="INFO")


class SlackChatPlatform(ChatPlatform):

    """Implementation of ChatPlatform for Slack.

    Attributes:
        client (WebClient): An instance of the WebClient class for making Slack API calls.
        channel_id (str): The ID of the channel for communication.

    Methods:
        __init__(self, token: str):
            Initializes a new instance of SlackPlatform with the provided token.

        connect(self, credentials: dict):
            Connects to Slack using the provided token.

            start_conversation(self, user_id: str):
            Starts a new conversation with the user by their id.
    """
    def __init__(self, credentials: dict):
        """
        Initializes a new instance of SlackChatPlatform.

        Args:
            credentials (dict): A dictionary containing necessary credentials, including 'client' for WebClient.

        """
        self.client = credentials.get("client")

    def connect(self, credentials: dict):
        """
        Connects to the Slack platform using the provided credentials.

        Args:
            credentials (dict): A dictionary containing necessary credentials for connecting to Slack.

        """
        pass

    def start_conversation(self, channel_id: str):
        """
        Starts a new conversation in the specified channel.

        Args:
            channel_id (str): The ID of the channel for starting the conversation.

        Returns:
            SlackConversation: An instance of SlackConversation representing the started conversation.

        """
        return SlackConversation(channel_id, self.client)


class SlackConversation(Conversation):
    """Represents a conversation on Slack."""
    def __init__(self, channel_id, client):
        """
        Initializes a new instance of the SlackConversation class.

        Args:
            channel_id (str): The ID of the Slack channel for the conversation.
            client: The Slack client used to interact with the Slack API.
        """
        self.channel_id = channel_id
        self.client = client

    def send_message(self, message_text: str, thread_ts: str = None):
        """
        Sends a message to the Slack channel.

        Args:
            message_text (str): The text of the message to be sent.
            thread_ts (str, optional): The timestamp of the thread to reply to, if any.
        """
        self.client.chat_postMessage(channel=self.channel_id, text=message_text, thread_ts=thread_ts)

    def receive_messages(self):
        """
        Placeholder method for receiving messages from the Slack channel.
        Actual implementation is missing as it depends on the specific requirements.
        """
        pass


class SlackMessage(Message):
    """Implementation of Message for Slack.

    Attributes:
    - message (dict): The Slack message dictionary.

    Methods:
        text(): Returns the text content of the message.
        user_id(): Returns the user ID of the user who sent the message.
    """

    def __init__(self, message):
        self.message = message

    @property
    def text(self):
        """Returns the text content of the message"""
        return self.message.get("text", "")

    @property
    def user_id(self):
        """Returns the user ID of the user who sent the message"""
        return self.message.get("user", "")


class SlackEventHandler:
    """
    A class for handling Slack events and messages.

    Attributes:
    - slack_chat_platform: The Slack chat platform instance.

    Methods:
        __init__(self, slack_chat_platform): Initializes the SlackEventHandler with the given Slack chat platform.
        handle_message(self, event_data): Handles incoming Slack messages and processes them accordingly.
    """
    def __init__(self, slack_chat_platform):
        """
        Initializes a new instance of the SlackEventHandler class.

        Parameters:
        - slack_chat_platform (obj): An instance of the Slack chat platform to be used for communication.
        """
        self.slack_chat_platform = slack_chat_platform

    def handle_message(self, event_data):
        """
        Handles incoming Slack messages and processes them.

        Parameters:
        - event_data (dict): The data representing the incoming Slack event.

        Details:
        - Extracts relevant information from the event data such as user ID, channel ID, and message text.
        - Logs the received question from the user.
        - Sends a response to the user acknowledging the received question.

        Note:
        - The actual processing logic for the question, including API requests, is currently commented out.

        Example:
        ```
        slack_handler = SlackEventHandler(slack_platform_instance)
        slack_handler.handle_message(event_data)
        ```

        """
        event = event_data["event"]
        channel_id = event.get("channel", "")
        user_id = event.get("user", "")
        text_data = event.get("text", "")
        # message_text = event["text"]
        # if "thread_ts" in event:
        #         thread_ts = event["thread_ts"]
        # else:
        #         thread_ts = event["ts"]

        if text_data:
            logger.info(f"Received a question from a user {user_id}: {text_data}")
            # Send request to API endpoint
            # uuid = message_text.strip().replace('UUID ', '')
            # requests.post('http://localhost:8000/api/v1/create_air_script/', data={'uuid': uuid,
            #                                                                            'thread_ts': thread_ts})

            if "thread_ts" not in event or event["ts"] == event["thread_ts"]:
                response_text = "Thanks for your question! We'll review it and respond shortly."
                self.slack_chat_platform.start_conversation(channel_id).send_message(response_text, thread_ts=event["ts"])
