import logging
import urllib
import pika
import gevent
import pickle

from django.core.paginator import Paginator
from django.conf import settings
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

    def on_join(self, thread, page_size=10, page=1):
        self.room = thread
        response = dict()

        messages = Message.objects.filter(thread=thread)
        response['action'] = 'connect'
        response['thread_id'] = thread

        self.broadcast_event_only_me('message', response)
        return True

    def on_message(self, message):
        self.log('User message: {0}'.format(message))
        data = dict()
        data['message'] = urllib.unquote(message['message'].encode('utf-8')).decode("utf-8")
        data['sender'] = message['sender']
        data['thread'] = message['thread']
        data['attachments'] = message.get('attachments', [])

        form = MessageForm(data=data)

        if form.is_valid():
            form.save()
            message.clear()
            message['msg'] = form.data
            message['action'] = 'new_message'
            self.broadcast_event('message', message)
            return True

    def on_mark_is_read(self, message_id, user_id):
        message = dict()

        try:
            msg = Message.objects.get(pk=message_id)
            if msg.sender.id != int(user_id):
                msg.is_read = True
                msg.save()
                message['action'] = 'is_read'
                message['message_id'] = message_id
        except:
            pass
        self.broadcast_event('message', message)
