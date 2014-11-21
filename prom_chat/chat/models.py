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
    members = models.ManyToManyField('auth.User', related_name='threads',
                                     verbose_name=_('Members'))


class Message(AuditFieldsMixin):
    sender = models.ForeignKey('account.User', related_name='sent_messages',
                               verbose_name=_('sender message'))
    message = models.TextField(verbose_name=_('Message'))
    is_read = models.BooleanField(default=False, verbose_name=_('Status read'))
    channel = models.ForeignKey(Channel, related_name='messages',
                                verbose_name=_('channel'))
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Message)
def send_to_socket(instance, created, **kwargs):
    """
    When create new Message, send to socket.
    """
    if created and not instance.is_read or not created and instance.is_read:
        parameters = pika.ConnectionParameters(settings.RABBIT_URL)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        for user in instance.thread.members.all():
            if user != instance.sender:
                # Set count_msg to Rabbit
                msg_count = Message.objects.get_not_read_message().exclude(sender=user).filter(thread__members=user).count()
                channel.queue_declare(queue='msg_count.{}'.format(user.pk))
                channel.basic_publish(exchange='',
                                      routing_key='msg_count.{}'.format(user.pk),
                                      body=unicode(msg_count))

            # Set thread in Rabbit
            channel.queue_declare(queue='thread.{}'.format(user.id))
            channel.basic_publish(exchange='',
                                  routing_key='thread.{}'.format(user.id),
                                  body=pickle.dumps(instance.thread))
        connection.close()
