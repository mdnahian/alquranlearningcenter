from flask import Blueprint, request, render_template, url_for, redirect
from blueprints import g
import json

landing_page = Blueprint('landing_page', __name__,  template_folder='../templates', static_folder='../static')


@landing_page.route('/')
def index():
    if g.current_user.is_authenticated:
        return redirect('/web')
    return render_template('template.html', page='index.html')


@landing_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect('/web')
    return render_template('template.html', page='login.html')


@landing_page.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        pass
    return render_template('template.html', page='signup.html')


@landing_page.route('/about')
def about():
    return render_template('template.html', page='about.html')


@landing_page.route('/contact')
def contact():
    return render_template('template.html', page='contact.html')