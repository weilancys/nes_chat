from flask_socketio import join_room, leave_room
from flask import request, session

USERS = {} # key is request.sid, value is user class

class User:
    def __init__(self, _id, nickname, room):
        self._id = _id
        self.nickname = nickname
        self.room = room


def is_user_already_online(nickname):
    for _id in USERS:
        if USERS[_id].nickname == nickname:
            return True
    return False


def add_user(user):
    USERS[request.sid] = user
    session['user'] = user
    join_room(user.room)


def remove_user():
    USERS.pop(session['user']._id)
    session.pop('user', None)
    #leave_room(session['user'].room)


def get_online_users():
    return USERS
