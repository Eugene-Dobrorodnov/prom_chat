from django import forms

from chat.models import Channel, Message


class ChannelForm(Channel):
    class Meta:
        model = Channel


class MessageForm(Message):
    class Meta:
        model = Message
