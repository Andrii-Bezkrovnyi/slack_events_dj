from django.urls import path
from .views import SlackEventView

urlpatterns = [
    path('slack/events/', SlackEventView.as_view(), name='slack_events'),
]
