from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .interfaces import ChatPlatform, Conversation, Message


class SlackPlatform(ChatPlatform):
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

    def __init__(self, token: str):
        """Initializes a new instance of SlackPlatform.

        Parameters:
            token (str): The Slack API token.
        """
        self.client = WebClient(token=token)
        self.channel_id = None

    def connect(self, credentials: dict):
        """Connects to Slack using the provided token.

        Parameters:
            credentials (dict): A dictionary containing the 'token' for authentication.
        """
        self.client = WebClient(token=credentials["token"])

    def start_conversation(self, user_id: str):
        """Starts a new conversation with the user by their id.

        Parameters:
            user_id (str): The ID of the user for the conversation.

        Returns:
            SlackConversation: An instance of the SlackConversation class for the started conversation.
        """
        self.channel_id = user_id
        return SlackConversation(self.client, self.channel_id)


class SlackConversation(Conversation):
    """Implementation of Conversation for Slack.

    Attributes:
        client (WebClient): The WebClient instance for interacting with the Slack API.
        channel_id (str): The ID of the Slack channel associated with this conversation.
    """

    def __init__(self, client: WebClient, channel_id: str):
        """Initializes a new instance of SlackConversation.

        Parameters:
            client (WebClient): The WebClient instance for interacting with the Slack API
            channel_id (str): The ID of the Slack channel associated with this conversation
        """
        self.client = client
        self.channel_id = channel_id

    def send_message(self, message_text: str):
        """Sends a message to the user within this conversation.

        Parameters:
            message_text (str): The text of the message to be sent
        """
        try:
            self.client.chat_postMessage(channel=self.channel_id, text=message_text)
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")

    def receive_messages(self):
        """Receives and returns a list of new messages from the user in this conversation.

        Returns:
            list: A list of SlackMessage objects representing received messages
        """
        try:
            response = self.client.conversations_history(channel=self.channel_id)
            messages = response["messages"]
            return [SlackMessage(message) for message in messages]
        except SlackApiError as e:
            print(f"Error getting messages: {e.response['error']}")


class SlackMessage(Message):
    """Implementation of Message for Slack.

    Attributes:
        message (dict): The Slack message dictionary.

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
