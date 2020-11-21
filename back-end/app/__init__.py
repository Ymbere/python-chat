from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = SocketIO()


def create_app(debug=False):
    app = Flask(__name__)
    cors = CORS(app)
    app.debug = debug
    app.config['SECRET_KEY'] = 'secret!'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(
        app,
        cors_allowed_origins="*"
    )
    return app
