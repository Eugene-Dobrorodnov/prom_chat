import logging
import urllib
import re
import metadata_parser
import json
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

    def emit_to_room_with_me(self, room, event, *args):
        """This is sent to all in the room (in this particular Namespace)"""
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        room_name = self._get_room_name(room)
        for sessid, socket in self.socket.server.sockets.iteritems():
            # print socket.session['rooms']
            # print '======================'
            # print room_name
            # print event
            # args.update({sessid: socket.session['rooms']})
            if 'rooms' not in socket.session:
                continue
            if room_name in socket.session['rooms']:
                socket.send_packet(pkt)


@namespace('/msg')
class MsgNamespace(BaseNamespace, RoomsMixin, BroadcastEventOnlyMyMixin):
    def initialize(self):
        self.logger = logging.getLogger("socketio.msg")
        self.log("Socketio session started")

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def on_join(self, room, channel_id):
        self.room = room
        self.join(room)

        response = {}

        messages = Message.objects.filter(channel=channel_id)
        result = render_to_string('chat/msg_list.html', {'messages': messages})
        response['action'] = 'connect'
        response['thread_id'] = channel_id
        response['result'] = result
        self.broadcast_event_only_me('message', response)
        return True

    def on_message(self, message):
        self.log('User message: {0}'.format(message))
        data = {}
        data['message'] = urllib.unquote(message['message'].encode('utf-8')).decode("utf-8")

        form = MessageForm(data)

        if form.is_valid():
            object = form.save(commit=False)
            object.sender_id = message['sender']
            object.channel_id = message['channel']
            object.save()
            message.clear()
            message['room'] = self._get_room_name(object.channel_id)
            message['action'] = 'new_message'
            message['result'] = render_to_string('chat/msg_detail.html',
                                                 {'msg': object})
            # parse url
            match = re.search(r'http://[a-zA-Z0-9]+\.[-a-zA-Z0-9_]+/*', object.message)
            if match:
                try:
                    url = metadata_parser.MetadataParser(url=object.message)
                    meta = url.metadata.get('meta')
                    page = url.metadata.get('page')
                    img = meta.get('og:image', None)
                    title =  urllib.unquote(page['title'].encode('utf-8')).decode("utf-8")
                    message['result'] = render_to_string('chat/url_parse.html',
                                                        {'img': img,
                                                         'title':title,
                                                         'obj': object})
                except:
                    pass

        else:
            message.clear()
            message['action'] = 'error'

        self.emit_to_room_with_me(object.channel_id, 'message', message)
        return True
