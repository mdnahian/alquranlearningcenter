from flask import Flask, render_template, url_for, request, redirect
from flask_login import *
from flask_socketio import SocketIO
from User import User
import os
import model
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'alquranlearningcenter'
login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app)


def get_next_session_from_sessions(sessions, uid='uid_student'):
    next_session = None
    # print sessions
    for session in sessions:
        user = User().get(session.get(uid))
        if user is not None:
            session['user'] = vars(user)

            d1 = datetime.strptime(session.get('datetime'), "%A %I:%M%p")
            d2 = d1 + timedelta(hours=int(session.get('duration')))
            current_d = datetime.now()
            
            # check if same day
            if session.get('datetime').split(' ')[0].strip() == current_d.strftime("%A"):
                # check if within time frame
                if current_d.time() >= d1.time() and current_d.time() <= d2.time():
                    next_session = session
    return next_session


# @app.context_processor
# def override_url_for():
#     return dict(url_for=dated_url_for)


# def dated_url_for(endpoint, **values):
#     if endpoint == 'static':
#         filename = values.get('filename', None)
#         if filename:
#             file_path = os.path.join(app.root_path,
#                                      endpoint, filename)
#             values['q'] = int(os.stat(file_path).st_mtime)
#     return url_for(endpoint, **values)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/dashboard') 
    return render_template('template.html', page='pages/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User(email=email, password=password)
        if email is not None and password is not None:
            if user.is_authenticated():
                login_user(user)
                return redirect('dashboard')
            else:
                return render_template('template.html', page='pages/login.html', msg='Email or password incorrect')
        else:
            return render_template('template.html', page='pages/login.html', msg='Please fill all fields')
    return render_template('template.html', page='pages/login.html')


@app.route('/signup')
def signup():
    return render_template('template.html', page='pages/signup.html')


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.account_type == 'teacher':
        sessions = model.Session(uid_teacher=current_user.uid).get_from_id(multiple=True)
        next_session = get_next_session_from_sessions(sessions)
        return render_template('template.html', page='pages/dash_teacher.html', sessions=sessions, next_session=next_session)
    elif current_user.account_type == 'student':
        sessions = model.Session(uid_student=current_user.uid).get_from_id(multiple=True)
        next_session = get_next_session_from_sessions(sessions, uid='uid_teacher')
        return render_template('template.html', page='pages/dash_student.html', next_session=next_session)
    elif current_user.account_type == 'admin':
        sessions = model.Session().get_from_id(get_all=True)
        return render_template('template.html', page='pages/dash_admin.html', sessions=sessions)
    else:
        return redirect('logout')

@app.route('/account')
@login_required
def account():
    return render_template('template.html', page='pages/account.html')

@app.route('/call/<sid>')
@login_required
def call(sid):
    session = model.Session(sid=sid).get_from_id()
    if current_user.account_type == 'teacher':
        return render_template('template.html', page='pages/call_teacher.html', session=session)
    elif current_user.account_type == 'student':
        return render_template('template.html', page='pages/call_student.html', session=session)


@socketio.on('enter')
def on_enter(enter):
    socketio.emit('new_user', enter)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
