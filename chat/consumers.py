from channels import Group
from channels.sessions import channel_session
from chat.models import Room, Message, GuestUser
from chat.views import get_client_ip
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from lazysignup.utils import is_lazy_user


# Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message):
    if is_lazy_user(message.user):
        guest = GuestUser.objects.get(ip_address=message.content['client'][0])
        message.channel_session['handle'] = guest.username
    else:
        message.channel_session['handle'] = 'Real User'
    try:
        # Work out room name from path (ignore slashes)
        split_path = message.content['path'].split("/")
        prefix = split_path[2]
        room = split_path[3]
        room_messages = Room.objects.get(slug=room).messages.all()
        message['text'] = room_messages
    except:
        return
    # Save room in session and add us to the group
    message.channel_session['room'] = room
    Group("%s" % room).add(message.reply_channel)

# Connected to websocket.receive
@channel_session_user_from_http
def ws_message(message):
    handle = message.channel_session.get('handle')
    room = Room.objects.get(slug=message.channel_session['room'])
    saved_message = Message.objects.create(room=room, handle=handle, message=message['text'])
    Group("%s" % message.channel_session['room']).send({
        "text": saved_message.message+'/'+saved_message.formatted_handle,
    })

# Connected to websocket.disconnect
@channel_session_user_from_http
def ws_disconnect(message):
    Group("%s" % message.channel_session['room']).discard(message.reply_channel)
