from django.conf.urls import url, include
from .views import chat

app_name = 'chat'
urlpatterns = [
    url(r'^chat/$', chat.ChatDashboardView.as_view(), name='chat-dashboard'),
    url(r'^chat/room/(?P<slug>[\w-]+)/$', chat.ChatRoomView.as_view(), name='chat-room'),
    url(r'^chat/convert/', include('lazysignup.urls')),
    url(r'^chat/room-autocomplete/(?P<name>[\w\ ]+)/$',chat.room_autocomplete,name='room-autocomplete'),
    url(r'^chat/room-subscribe/(?P<slug>[\w-]+)/$',chat.room_subscribe ,name='room-subscribe'),
    url(r'^chat/room-unsubscribe/(?P<slug>[\w-]+)/$',chat.room_unsubscribe ,name='room-unsubscribe'),
]
