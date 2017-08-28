from flask import Flask
from blueprints.landing import landing_page
from blueprints.dashboard import dashboard
from blueprints import g
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import *
from flask_socketio import SocketIO
from LinxUser import User

app = Flask(__name__)
app.secret_key = 'alquranlearningcenter'
login_manager = LoginManager()
app.register_blueprint(landing_page)
app.register_blueprint(dashboard)
bcrypt = Bcrypt(app)
mongo = PyMongo(app)
login_manager.init_app(app)
socketio = SocketIO(app)


@app.before_request
def before_request():
    g.mongo = mongo
    g.bcrypt = bcrypt
    g.login_manager = login_manager
    g.socketio = socketio
    g.current_user = current_user


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.run(debug=True)