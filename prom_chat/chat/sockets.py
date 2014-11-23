import logging
import urllib
import pika
import gevent
import pickle

from django.template.loader import render_to_string

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace

from chat.models import Channel, Message
from chat.forms import MessageForm


class BroadcastEventOnlyMyMixin(BroadcastMixin):

    def broadcast_event_only_me(self, event, *args):
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)

        for sessid, socket in self.socket.server.sockets.iteritems():
            if socket is self.socket:
                socket.send_packet(pkt)


@namespace('/msg')
class MsgNamespace(BaseNamespace, RoomsMixin, BroadcastEventOnlyMyMixin):
    def initialize(self):
        self.logger = logging.getLogger("socketio.msg")
        self.log("Socketio session started")

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def on_join(self, channel, page_size=10, page=1):
        self.room = channel
        response = dict()

        messages = Message.objects.filter(channel=channel)
        result = render_to_string('chat/msg_list.html', {'messages': messages})
        response['action'] = 'connect'
        response['thread_id'] = channel
        response['result'] = result
        self.broadcast_event_only_me('message', response)
        return True

    def on_message(self, message):
        self.log('User message: {0}'.format(message))
        data = dict()
        data['message'] = urllib.unquote(message['message'].encode('utf-8')).decode("utf-8")

        form = MessageForm(data)

        if form.is_valid():
            object = form.save(commit=False)
            object.sender_id = message['sender']
            object.channel_id = message['channel']
            object.save()
            message.clear()
            message['action'] = 'new_message'
            message['result'] = render_to_string('chat/msg_detail.html',
                                                 {'msg': object})
        else:
            message.clear()
            message['action'] = 'error'

        self.broadcast_event('message', message)
        return True

    # def recv_disconnect(self):
    #     self.log('Disconnected')
    #     self.connection.close()
    #     self.disconnect(silent=True)
    #     return True
