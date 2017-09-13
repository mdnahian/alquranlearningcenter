from flask import Blueprint, request, render_template, url_for, redirect
from blueprints import g
from LinxUser import User
import json


dashboard = Blueprint('dashboard', __name__, url_prefix='/web', template_folder='../templates', static_folder='../static')


@dashboard.route('/')
def web():
	if g.isLoggedIn() is False:
		return redirect(url_for('landing_page.index'))
	if 'specifics' in g.session['user']:
		return render_template('template.html', page='dashboard.html', current_user=g.session['user'], next_session=None)
	else:
		return redirect(url_for('dashboard.specifics'))

@dashboard.route('/account')
def account():
	if g.isLoggedIn() is False:
		return redirect(url_for('landing_page.index'))
	return render_template('template.html', page='account.html', current_user=g.session['user'])


@dashboard.route('/specifics', methods=['GET', 'POST'])
def specifics():
	if g.isLoggedIn() is False:
		return redirect(url_for('landing_page.index'))
	if 'specifics' in g.session['user']:
		return redirect(url_for('dashboard.web'))
	if request.method == 'POST':
		s = request.get_json()
		g.mongo.db.alquranlearningcenter.users.update_one({'email': g.session['user']['email']}, {"$set": {'specifics': s}}, upsert=False)
		
		user = g.mongo.db.alquranlearningcenter.users.find_one({"email": g.session['user']['email']})
		user['_id'] = False
		g.session.clear()
		g.session['user'] = user
		g.current_user = user
		return g.success_msg({'email': g.session['user']['email']})
	return render_template('template.html', page='specifics.html', current_user=g.session['user'])


@dashboard.route('/logout')
def logout():
	if g.isLoggedIn():
		g.session.clear()
		redirect('login')
	return redirect('/')