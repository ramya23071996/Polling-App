from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
import redis

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")

    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)

    from .routes import main
    from .socketio_events import register_socketio_events

    app.register_blueprint(main)
    register_socketio_events(socketio)

    return app