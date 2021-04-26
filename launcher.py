from nes_chat import create_app
from nes_chat.chat import socketio

if __name__ == "__main__":
    app = create_app()
    # socketio.init_app(app)
    socketio.run(app)