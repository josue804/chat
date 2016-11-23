from django.conf.urls import url
from .views import ChatRoomView

app_name = 'chat'
urlpatterns = [
    url(r'^$', ChatRoomView.as_view(), name='chat-room'),
]
