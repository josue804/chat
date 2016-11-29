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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    request.session['client_ip'] = ip
    return ip

def get_or_create_guest_account(user, request):
    client_ip = get_client_ip(request)
    try:
        guest_user = GuestUser.objects.get(ip_address=client_ip)
        return guest_user.username
    except:
        haikunator = Haikunator()
        guest_name = haikunator.haikunate(token_length=0)
        guest_user = GuestUser.objects.create(username=guest_name, temp_token=user.username, ip_address=client_ip)
        return guest_user.username

@method_decorator(allow_lazy_user, name='dispatch')
class ChatRoomView(FormView):
    template_name = "chat-room.html"
    form_class = ChatRoomForm

    def get_context_data(self, *args, **kwargs):
        kwargs = super(ChatRoomView, self).get_context_data(*args, **kwargs)
        room = Room.objects.get(slug=self.kwargs['slug'])
        kwargs['messages'] = room.messages.all().order_by('timestamp')
        kwargs['room'] = room
        if is_lazy_user(self.request.user):
            kwargs['username'] = get_or_create_guest_account(self.request.user, self.request)
        return kwargs


@method_decorator(allow_lazy_user, name='dispatch')
class ChatDashboardView(TemplateView):
    template_name = "chat-dashboard.html"

    def get_context_data(self, *args, **kwargs):
        kwargs = super(ChatDashboardView, self).get_context_data(*args, **kwargs)
        if is_lazy_user(self.request.user):
            kwargs['username'] = get_or_create_guest_account(self.request.user, self.request)
        return kwargs

    def post(self, form):
        unslugified_room = form.POST.get('room')
        room_slug = slugify(unslugified_room)
        Room.objects.get_or_create(name=unslugified_room, slug=room_slug)
        return redirect('chat:chat-room', slug=room_slug)
