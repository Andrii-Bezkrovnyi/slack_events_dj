from django.urls import path
from .views import SlackMessageHandler

urlpatterns = [
    path('slack/events/', SlackMessageHandler.as_view(), name='slack_events'),
]
