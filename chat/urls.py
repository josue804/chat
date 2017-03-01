from django.conf.urls import url, include
from .views import core, chat

app_name = 'chat'
urlpatterns = [
    url(r'^$', chat.ChatDashboardView.as_view(), name='chat-dashboard'),
    url(r'^(?P<slug>[\w-]+)/$', chat.ChatRoomView.as_view(), name='chat-room'),
    url(r'^convert/', include('lazysignup.urls')),
    url(r'^room-autocomplete/(?P<name>[\w\ ]+)/$',chat.room_autocomplete,name='room-autocomplete'),
    url(r'^$', core.DashboardView.as_view(), name='dashboard'),
]
