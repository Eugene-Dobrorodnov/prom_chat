from django import forms

from chat.models import Channel, Message


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class' : 'msg-textarea'})
