from flask import Blueprint, request, render_template, url_for, redirect
from web.blueprints import g
from web.User import User
import json

landing_page = Blueprint('landing_page', __name__,  template_folder='../templates', static_folder='../static')


BASE_URL = 'https://alquranlearningcenter.com'


@landing_page.route('/')
def index():
    if g.isLoggedIn():
        return redirect('/web')
    return render_template('template.html', page='index.html', current_user=None, num_teachers=14, num_students=52)


@landing_page.route('/login', methods=['GET', 'POST'])
def login():
    if g.isLoggedIn():
        return redirect('/web')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User(email, password)
        is_authenticated, response = user.authenticate()
        if is_authenticated:
            g.session['user'] = user.obj
            g.current_user = user.obj
            return redirect('/web')
        else:
            return response
    return render_template('template.html', page='login.html', current_user=None)




@landing_page.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.isLoggedIn():
        return redirect('/web')
    if request.method == 'POST':
        u = request.get_json()
        u['isConfirmed'] = False
        u['isSuspended'] = False

        if u.get('password') == u.get('confirm'):

            user = g.mongo.db.alquranlearningcenter.users.find_one({"email": u.get('email')})

            if user is None:

                password = g.bcrypt.generate_password_hash(u.get('password'))
                confirmation_key = g.generate_random()
		
                u['password'] = password
                u['confirmation_key'] = confirmation_key

                user_id = g.mongo.db.alquranlearningcenter.users.insert_one(u)

                if user_id is not None:
		    confirmation_url = BASE_URL + '/confirm/' + u['email'] + '/' + confirmation_key
		    g.send_email([u['email']], 'Welcome to Al-Quran Learning Center', '''
			Hello,<br><br>
		You've just created an account on <a href="''' + BASE_URL + '''">Al-Quran Learning Center</a> but there's still one more step before you can start.<br><br>
		Please confirm your email address by following this link:<br>
		<a href="''' + confirmation_url + '''">''' + confirmation_url + '''</a>
		<br><br>
		Thanks,
		A.L.C. Team
		<br><br>
		<small>P.S. If you did not make an account, please disregard this email.</small>
		    ''')
                    return g.success_msg({'email': u['email']})
                else:
                    return g.error_msg('An unexpected error has occured.')
            else:
                return g.error_msg('A user is already registered with this email.')
        else:
            return g.error_msg('Passwords do not match.')
    return render_template('template.html', page='signup.html', current_user=None)


@landing_page.route('/success/<email>')
def success(email):
    if g.isLoggedIn():
        return redirect('/web')
    return render_template('template.html', page='success.html', current_user=None, email=email)



@landing_page.route('/confirm/<email>/<confirmation_key>')
def confirm(email, confirmation_key):
    user = g.mongo.db.alquranlearningcenter.users.find_one({"email": email, "confirmation_key": confirmation_key})
    if user is not None:
        g.mongo.db.alquranlearningcenter.users.update_one({"email": email}, {"$set": {"isConfirmed": True}})
        return redirect(url_for('landing_page.login'))
    return g.error_msg('the user does not exist')





@landing_page.route('/about')
def about():
    current_user = None
    if g.isLoggedIn():
        current_user = g.session['user']
    return render_template('template.html', page='about.html', current_user=current_user)


@landing_page.route('/contact')
def contact():
    current_user = None
    if g.isLoggedIn():
        current_user = g.session['user']
    return render_template('template.html', page='contact.html', current_user=current_user)
