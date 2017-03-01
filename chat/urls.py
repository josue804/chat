from django.conf.urls import url, include
from .views import chat

app_name = 'chat'
urlpatterns = [
    url(r'^chat/$', chat.ChatDashboardView.as_view(), name='chat-dashboard'),
    url(r'^chat/room/(?P<slug>[\w-]+)/$', chat.ChatRoomView.as_view(), name='chat-room'),
    url(r'^chat/convert/', include('lazysignup.urls')),
    url(r'^chat/room-autocomplete/(?P<name>[\w\ ]+)/$',chat.room_autocomplete,name='room-autocomplete'),
]
