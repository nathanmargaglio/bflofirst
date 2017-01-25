from flask_socketio import SocketIO, emit
from models import Owner, Listing, Parcel, User, Log, db, FacebookLead, Property, Chat
from main import current_user
import datetime
from config import local_cities, admins

socketio = SocketIO()

# SOCKET-IO
@socketio.on('init_connect')
def init_connect(json):
    print current_user.email
    current_user.room = json['room']
    db.session.add(current_user)
    db.session.commit()

    if current_user.room == '0':
        greeting = """ Greetings!  You have opened BDS's new chat module. It has been painfully coded from scratch by Nate, and as such is probably buggy as hell. Consider this module in alpha stages, as it does not have the features required to be of much use.  But play around with it and let me know if there is anything I can add to get it up to spec.
Only the last 10 messages will appear.  Click the load button for the 100 most recent messages.  Adding an integer to the text box then pressing load will load that many most recent messages.
- Nate
"""
    elif current_user.room == '1':
        greeting = """You've entered the Follow Up room!  We'll add functionality to organize follow ups on leads here."""
    elif current_user.room == '2':
        greeting = """Heres our "Other" room.  So, other discussion is here."""
    else:
        greeting = "You've been connected to room " + str(current_user.room)

    emit('my_response', {'user': "Admin", 'data': greeting, 'room': current_user.room})

    for c in Chat.query.filter(Chat.room == current_user.room).order_by(Chat.time).all()[-10:]:
        emit('my_response', {'user': c.user + " ({})".format(c.time - datetime.timedelta(hours=5)), 'data': c.message,
                             'room': current_user.room})


@socketio.on('connect')
def connect():
    print "CONNECTED!"


@socketio.on('load')
def loadposts(json):
    room = json['room']
    current_user.room = room
    db.session.add(current_user)
    db.session.commit()
    try:
        limit = int(json['data'])
    except:
        limit = 100

    loaded = ""
    for c in Chat.query.filter(Chat.room == room).order_by(Chat.time).all()[-limit:]:
        loaded += c.user + " ({}): ".format(c.time - datetime.timedelta(hours=5)) + c.message + "\n"

    emit('my_response', {'user': "Loaded", 'data': "Room " + str(room) + "\n" + loaded, 'room': current_user.room})


@socketio.on('to_server')
def newpost(json):
    if json['data'][0] == '~':
        if current_user.email in admins:
            current_user.room = -1
            db.session.add(current_user)
            db.session.commit()
            emit('shell', {'user': current_user.email, 'data': "<b>Entered Command Mode.<b>", 'room': -1})
            return

    if current_user.room == '-1':
        emit('my_response', {'user': current_user.email, 'data': json['data'], 'room': current_user.room},
             broadcast=True)
        try:
            for i in db.engine.execute(json['data']):
                emit('my_response', {'user': "SQL", 'data': str(i), 'room': -1}, broadcast=True)
        except Exception as e:
            emit('my_response', {'user': "SQL", 'data': str(e), 'room': -1}, broadcast=True)
        return

    try:
        user = current_user.email
    except:
        user = "Anon"
    try:
        c = Chat()
        c.user = user
        c.message = json['data']
        c.room = json['room']
        c.time = datetime.datetime.now()
        db.session.add(c)
        db.session.commit()
    except:
        pass
    emit('my_response', {'user': user, 'data': json['data'], 'room': current_user.room}, broadcast=True)


@socketio.on('shell')
def shell(json):
    try:
        for i in db.engine.execute(json['data']):
            print i
    except Exception as e:
        print e
