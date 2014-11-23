import pika
import pickle

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django.conf import settings


class AuditFieldsMixin(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Channel(AuditFieldsMixin):
    title = models.CharField(max_length=255, verbose_name=_('title'))

    def __unicode__(self):
        return self.title


class Message(AuditFieldsMixin):
    sender = models.ForeignKey('auth.User', related_name='sent_messages',
                               verbose_name=_('sender message'))
    message = models.TextField(verbose_name=_('Message'))
    channel = models.ForeignKey(Channel, related_name='messages',
                                verbose_name=_('channel'))

    class Meta:
        ordering = ('create_at',)

    def __unicode__(self):
        return self.message


@receiver(post_save, sender=Message)
def send_to_socket(instance, created, **kwargs):
    """
    When create new Message, send to socket.
    """
    if created:
        parameters = pika.ConnectionParameters(settings.RABBIT_URL)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        connection.close()
