from flask import render_template, request, url_for, redirect, flash, session, abort, jsonify
from flask.blueprints import Blueprint
from flask_socketio import SocketIO, emit, join_room, leave_room
from .users import User
import time
import json

bp = Blueprint("chat", __name__)
socketio = SocketIO()

@bp.route('/')
def chat_lobby():
    return render_template('chat/lobby.html')


@bp.route('/chat', methods=("POST", ))
def chat_room():
    nickname = request.form.get('nickname')
    room = request.form.get('room')

    if nickname is None or room is None:
        abort(400)

    if User.is_user_already_online(nickname):
        flash("user is already online.", 'error')
        return redirect(url_for('chat.chat_lobby'))

    return render_template('chat/room.html', nickname=nickname, room=room)


@socketio.on('connect')
def user_connect_handler():
    pass


@socketio.on('join')
def user_join_handler(nickname, room):
    user = User(request.sid, nickname, room)
    if not User.add_user(user):
        flash("user is already online.", 'error')
        return redirect(url_for('chat.chat_lobby'))
    update_user_list(user.room)

@socketio.on('disconnect')
def user_disconnect_handler():
    user = User.get_current_user()
    User.remove_user()
    update_user_list(user.room)


@socketio.on('chat-msg')
def chat_msg_handler(msg, nickname, room):
    ts = time.time()
    socketio.emit('chat-msg', (msg, nickname, room, ts), room=room)
    

def update_user_list(room):
    room_users = User.get_room_users(room)
    users = []
    for _id, user in room_users.items():
        users.append(user.nickname)
    socketio.emit('update-users-list', users, room=room)