from flask import Blueprint, request, render_template, url_for, redirect
from web.blueprints import g
import os
import re

dashboard = Blueprint('dashboard', __name__, url_prefix='/web', template_folder='../templates', static_folder='../static')

@dashboard.route('/')
def web():
	print g
	if g.isLoggedIn() is False:
		return redirect(url_for('landing_page.index'))
	if g.session['user']['accountType'] == 'admin':
		return redirect(url_for('admin.panel'))
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


@dashboard.route('/call')
def call():
	if g.isLoggedIn() is False:
		return redirect(url_for('landing_page.index'))
	if g.session['user']['accountType'] == 'teacher':
		return render_template('template.html', page='call_teacher.html', current_user=g.session['user'])
	elif g.session['user']['accountType'] == 'student':
		return render_template('template.html', page='call_student.html', current_user=g.session['user'])
	# if 'sessions' in g.session['user']:
	# 	pass
	# else:
	# 	pass



def sortby(x):
    try:
	num = int(re.search(r'\d+', x).group())
	#print num
        return num
    except ValueError:
        return float('inf')


@dashboard.route('load_pages', methods=['POST'])
def load_pages():
	if request.method == 'POST':
		resource = request.form['resource']
		resource = re.sub('[\?].+', '', resource)
		static_dir = os.path.dirname(resource)
		directory = '/var/www/alquranlearningcenter/app/web' + static_dir
		files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
		files.sort(key=sortby)
		for i in range(0, len(files)):
			files[i] = static_dir + '/' + files[i]
		return g.success_msg(files)
	return g.error_msg('failed to load')

@dashboard.route('/logout')
def logout():
	if g.isLoggedIn():
		g.session.clear()
		redirect('login')
	return redirect('/')
