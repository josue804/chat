from channels import Group
from channels.sessions import channel_session

# Connected to websocket.connect
@channel_session
def ws_connect(message):
    # Work out room name from path (ignore slashes)
    split_path = message.content['path'].split("/")
    prefix = split_path[2]
    room = split_path[3]
    # Save room in session and add us to the group
    message.channel_session['room'] = room
    Group("%s" % room).add(message.reply_channel)

# Connected to websocket.receive
@channel_session
def ws_message(message):
    Group("%s" % message.channel_session['room']).send({
        "text": message['text'],
    })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("%s" % message.channel_session['room']).discard(message.reply_channel)
