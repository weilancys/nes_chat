from flask import Flask
from .chat import bp as chat_bp
from .chat import socketio


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = 'dev'

    app.register_blueprint(chat_bp)

    socketio.init_app(app)

    return app