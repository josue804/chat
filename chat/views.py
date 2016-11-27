from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils.text import slugify
from .models import Room, Message
from lazysignup.decorators import allow_lazy_user
from django.utils.decorators import method_decorator


@method_decorator(allow_lazy_user, name='dispatch')
class ChatRoomView(TemplateView):
    template_name = "chat-room.html"

    def get_context_data(self, *args, **kwargs):
        kwargs = super(ChatRoomView, self).get_context_data(*args, **kwargs)
        room = Room.objects.get(slug=kwargs['slug'])
        kwargs['messages'] = room.messages.all()
        kwargs['room'] = room
        return kwargs

@method_decorator(allow_lazy_user, name='dispatch')
class ChatDashboardView(TemplateView):
    template_name = "chat-dashboard.html"

    def get_context_data(self, *args, **kwargs):
        kwargs = super(ChatDashboardView, self).get_context_data(*args, **kwargs)
        return kwargs

    def post(self, form):
        unslugified_room = form.POST.get('room')
        room_slug = slugify(unslugified_room)
        Room.objects.get_or_create(name=unslugified_room, slug=room_slug)
        return redirect('chat:chat-room', slug=room_slug)
