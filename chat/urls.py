from django.conf.urls import url, include
from .views import ChatRoomView, ChatDashboardView

app_name = 'chat'
urlpatterns = [
    url(r'^$', ChatDashboardView.as_view(), name='chat-dashboard'),
    url(r'^(?P<slug>[\w-]+)/$', ChatRoomView.as_view(), name='chat-room'),
    url(r'^convert/', include('lazysignup.urls')),
]
