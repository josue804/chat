from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class ChatRoomView(TemplateView):
    template_name = "chat-room.html"
