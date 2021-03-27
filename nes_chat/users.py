from flask_socketio import join_room, leave_room
from flask import request, session

USERS = {} # key is request.sid, value is user class instance

class User:
    def __init__(self, _id, nickname, room):
        self._id = _id
        self.nickname = nickname
        self.room = room


    @staticmethod
    def is_user_already_online(nickname):
        for _id in USERS:
            if USERS[_id].nickname == nickname:
                return True
        return False

    @staticmethod
    def add_user(user):
        if User.is_user_already_online(user.nickname):
            return False
        USERS[request.sid] = user
        session['current_io_user'] = user
        join_room(user.room)
        return True

    @staticmethod
    def remove_user():
        leave_room(session['current_io_user'].room)
        USERS.pop(session['current_io_user']._id, None)
        session.pop('current_io_user', None)

    @staticmethod
    def get_online_users():
        return USERS

    @staticmethod
    def get_room_users(room):
        room_users = {}
        for _id in USERS:
            if USERS[_id].room == room:
                room_users[_id] = USERS[_id]
        return room_users
        
    @staticmethod
    def get_current_user():
        return session['current_io_user']