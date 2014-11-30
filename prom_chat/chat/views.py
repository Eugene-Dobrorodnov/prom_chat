from django.shortcuts import get_object_or_404, HttpResponse
from django.views.generic import ListView, View, CreateView
from django.template.loader import render_to_string

from chat.models import Channel
from chat.forms import MessageForm, ChannelForm
from common.mixins import AjaxRequiredMixin, LoginRedirectMixin


class ChatView(LoginRedirectMixin, ListView):
    model = Channel
    context_object_name = 'channels'
    template_name = 'chat/channels_list.html'


class ChannelDetail(LoginRedirectMixin, AjaxRequiredMixin, View):
    template_name = 'chat/channel_detail.html'

    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, pk=kwargs['pk'])
        context = {
            'channel': channel,
            'request': request,
            'form': MessageForm
        }
        html = render_to_string('chat/channel_detail.html', context)
        return HttpResponse(html)


class CreateChannelView(LoginRedirectMixin, AjaxRequiredMixin, CreateView):
    model = Channel
    form_class = ChannelForm

    def get(self, *args, **kwargs):
        html = render_to_string('chat/channel_create.html',
                                {'form': self.form_class})
        return HttpResponse(html)

    def form_invalid(self, form):
        return HttpResponse(status=400)

    def form_valid(self, form):
        object = form.save()
        html = render_to_string('chat/channel_create_success.html',
                                {'channel': object})
        return HttpResponse(html)

chat_home = ChatView.as_view()
chat_room = ChannelDetail.as_view()
create_channel = CreateChannelView.as_view()
