from flask import Flask
from .chat import bp as chat_bp
from .chat import socketio


def create_app(test_config=None):
    app = Flask(__name__)

    # config
    app.config["SECRET_KEY"] = 'dev'

    # blueprints / routes
    app.register_blueprint(chat_bp)

    # extensions
    socketio.init_app(app) # add flask-socketio support outside of create_app function

    return app