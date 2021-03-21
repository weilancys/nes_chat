from flask import render_template, request, url_for, redirect, flash, session
from flask.blueprints import Blueprint
from flask_socketio import SocketIO, emit, join_room, leave_room
from .users import User, add_user, remove_user, get_online_users, is_user_already_online

bp = Blueprint("chat", __name__)
socketio = SocketIO()

@bp.route('/')
def chat_lobby():
    return render_template('chat/lobby.html')


@bp.route('/chat', methods=("POST", ))
def chat_room():
    nickname = request.form.get('nickname')
    room = request.form.get('room')

    if is_user_already_online(nickname):
        flash("user is already online.", 'error')
        return redirect(url_for('chat.chat_lobby'))

    return render_template('chat/room.html', nickname=nickname, room=room)


@socketio.on('connect')
def user_connect_handler():
    pass


@socketio.on('join')
def user_join_handler(nickname, room):
    user = User(request.sid, nickname, room)
    add_user(user)
    print(session['user'].nickname + " has joined.")


@socketio.on('disconnect')
def user_disconnect_handler():
    print(f"${session['user'].nickname} has left.")
    remove_user()


@socketio.on('chat-msg')
def chat_msg_handler(msg):
    pass

