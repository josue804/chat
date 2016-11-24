from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils.text import slugify
from .models import Room, Message
# Create your views here.
class ChatRoomView(TemplateView):
    template_name = "chat-room.html"

    def get_context_data(self, *args, **kwargs):
        kwargs = super(ChatRoomView, self).get_context_data(*args, **kwargs)
        room = Room.objects.get(slug=kwargs['slug'])
        kwargs['messages'] = room.messages.all()
        return kwargs

# Create your views here.
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
