from nes_chat import create_app
from flask_socketio import SocketIO

# application = create_app()
# socketio = SocketIO(app=application)
# socketio.run(application)

if __name__ == "__main__":
    app = create_app()
    socketio = SocketIO(app)
    socketio.run(app)