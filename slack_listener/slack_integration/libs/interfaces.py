from abc import ABC, abstractmethod


class ChatPlatform(ABC):
    """Abstract base class for chat platforms.

    Methods:
      connect(self, credentials: dict):
          Connects to the chat platform using the provided credentials.
      start_conversation(self, user_id: str):
          Starts a new conversation with the user by their id.
    """

    @abstractmethod
    def connect(self, credentials: dict):
        """Connects to the chat platform using the provided credentials."""

    @abstractmethod
    def start_conversation(self, user_id: str):
        """Starts a new conversation with the user by their id."""


class Conversation(ABC):
    """Represents a conversation thread with a user"""

    @abstractmethod
    def send_message(self, message_text: str):
        """Sends a message to the user within this conversation.

        Parameters:
            message_text (str): The text of the message to be sent
        """

    @abstractmethod
    def receive_messages(self):
        """Receives and returns a list of new messages from the user in this conversation.

        Returns:
            list: A list of messages received from the user
        """


class Message(ABC):
    """Represents a message within a conversation.

    Attributes:
        text (str): Returns the text content of the message.
        user_id (str): Returns the user ID of the user who sent the message.
    """

    @property
    @abstractmethod
    def text(self):
        """Returns the text content of the message"""

    @property
    @abstractmethod
    def user_id(self):
        """Returns the user ID of the user who sent the message"""
