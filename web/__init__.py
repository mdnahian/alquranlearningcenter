from flask import Flask, session, url_for
from web.blueprints.landing import landing_page
from web.blueprints.dashboard import dashboard
from web.blueprints import g
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from LinxUser import User
import os



app = Flask(__name__)
app.secret_key = 'alquranlearningcenter'
app.register_blueprint(landing_page)
app.register_blueprint(dashboard)
bcrypt = Bcrypt(app)
mongo = PyMongo(app)
socketio = SocketIO(app)




@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.before_request
def before_request():
    g.mongo = mongo
    g.bcrypt = bcrypt
    g.socketio = socketio
    g.session = session


if __name__ == '__main__':
    app.run(debug=True)
