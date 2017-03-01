from channels import Group
from channels.sessions import channel_session
from .models import Room, Message, GuestUser
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from lazysignup.utils import is_lazy_user
from django.db.models import F
from django.utils.safestring import mark_safe

# Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message):
    if is_lazy_user(message.user):
        client_ip = message.http_session['client_ip']
        guest = GuestUser.objects.get(ip_address=client_ip)
        message.channel_session['handle'] = guest.username
    else:
        message.channel_session['handle'] = message.user.username
    try:
        # Work out room name from path (ignore slashes)
        split_path = message.content['path'].split("/")
        prefix = split_path[2]
        room_slug = split_path[4]
        room = Room.objects.get(slug=room_slug)
        room.add_connection()
        room_messages = room.messages.all()
        message['text'] = room_messages
    except:
        return
    # Save room in session and add us to the group
    message.channel_session['room'] = room.slug
    Group("%s" % room.slug).add(message.reply_channel)

# Connected to websocket.receive
@channel_session_user_from_http
def ws_message(message):
    handle = message.channel_session.get('handle')
    room = Room.objects.get(slug=message.channel_session['room'])
    saved_message = Message.objects.create(room=room, handle=handle, message=message['text'])
    Group("%s" % message.channel_session['room']).send({
        "text": saved_message.message+'GqbTvLGBHZ'+saved_message.formatted_handle,
    })

# Connected to websocket.disconnect
@channel_session_user_from_http
def ws_disconnect(message):
    split_path = message.content['path'].split("/")
    room_slug = split_path[4]
    try:
        Room.objects.get(slug=room_slug).remove_connection()
        Group("%s" % message.channel_session['room']).discard(message.reply_channel)
    except:
        pass
