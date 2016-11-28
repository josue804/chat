from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.text import slugify
from .models import Room, Message, GuestUser
from lazysignup.decorators import allow_lazy_user
from lazysignup.templatetags.lazysignup_tags import is_lazy_user
from django.utils.decorators import method_decorator
from haikunator import Haikunator
from .forms import ChatRoomForm

def get_or_create_guest_account(user):
    try:
        guest_user = GuestUser.objects.get(temp_token=user.username)
        return guest_user.name
    except:
        haikunator = Haikunator()
        guest_name = haikunator.haikunate(token_length=0)
        GuestUser.objects.create(name=guest_name, temp_token=user.username)
        return guest_name

@method_decorator(allow_lazy_user, name='dispatch')
class ChatRoomView(FormView):
    template_name = "chat-room.html"
    form_class = ChatRoomForm

    def get_context_data(self, *args, **kwargs):
        kwargs = super(ChatRoomView, self).get_context_data(*args, **kwargs)
        room = Room.objects.get(slug=self.kwargs['slug'])
        kwargs['messages'] = room.messages.all()
        kwargs['room'] = room
        if is_lazy_user(self.request.user):
            kwargs['guest_name'] = get_or_create_guest_account(self.request.user)
            kwargs['gt'] = self.request.user.username
        return kwargs


@method_decorator(allow_lazy_user, name='dispatch')
class ChatDashboardView(TemplateView):
    template_name = "chat-dashboard.html"

    def get_context_data(self, *args, **kwargs):
        kwargs = super(ChatDashboardView, self).get_context_data(*args, **kwargs)
        if is_lazy_user(self.request.user):
            kwargs['guest_name'] = 'Guest ' + get_or_create_guest_account(self.request.user)
        return kwargs

    def post(self, form):
        unslugified_room = form.POST.get('room')
        room_slug = slugify(unslugified_room)
        Room.objects.get_or_create(name=unslugified_room, slug=room_slug)
        return redirect('chat:chat-room', slug=room_slug)
