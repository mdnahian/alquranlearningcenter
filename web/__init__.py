from flask import Flask, render_template, url_for, request, redirect
from flask_login import *
from User import User
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
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
    return render_template('template.html', page='pages/dashboard.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('index')



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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)