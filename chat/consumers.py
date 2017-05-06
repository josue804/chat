from channels import Group
from channels.sessions import channel_session
from .models import Room, Message, GuestUser, CustomUser
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from lazysignup.utils import is_lazy_user
from django.db.models import F
from django.utils.safestring import mark_safe

# Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message):
    if '/room/' not in message.content['path']:
        return
    message.channel_session['handle'] = message.user.get_username()
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
@channel_session_user
def ws_message(message):
    handle = message.channel_session.get('handle')
    if message.user.is_anonymous():
        user = CustomUser.objects.get(nickname=handle)
    else:
        user = message.user
    room = Room.objects.get(slug=message.channel_session['room'])
    saved_message = Message.objects.create(room=room, handle=handle, message=message['text'], user=user)
    handle = user.get_username()
    Group("%s" % message.channel_session['room']).send({
        "text": saved_message.message+'GqbTvLGBHZ'+saved_message.formatted_handle+'GqbTvLGBHZ'+handle,
    });

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    if '/room/' not in message.content['path']:
        return
    split_path = message.content['path'].split("/")
    room_slug = split_path[4]
    try:
        Room.objects.get(slug=room_slug).remove_connection()
        Group("%s" % message.channel_session['room']).discard(message.reply_channel)
    except:
        pass
