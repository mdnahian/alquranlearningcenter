from flask import Blueprint, request, render_template, url_for, redirect
from web.blueprints import g
from datetime import datetime, timedelta
import time
import braintree
import os
import re

dashboard = Blueprint('dashboard', __name__, url_prefix='/web', template_folder='../templates', static_folder='../static')
gateway = braintree.BraintreeGateway(access_token='access_token$sandbox$9yjs46kcxryg9t8h$84cf0b13ee2264a3f2dbf31babeaf274')

@dashboard.route('/')
def web():
	if g.isLoggedIn() is False:
		return redirect(url_for('landing_page.index'))
	u = g.mongo.db.alquranlearningcenter.users.find_one({'email': g.session['user']['email']})
	u['_id'] = False
	g.session['user'] = u
	if 'specifics' not in g.session['user']:
		return redirect(url_for('dashboard.specifics'))
	if g.session['user']['accountType'] == 'admin':
		return redirect(url_for('admin.panel'))
	if g.session['user']['accountType'] == 'student' and ('total_sessions' not in g.session['user'] or 'last_paid' not in g.session['user']):
		return redirect(url_for('dashboard.plans'))
	if g.session['user']['accountType'] == 'student' and g.check_date(g.session['user']['last_paid']) == False:
		return redirect(url_for('dashboard.plans'))
	session_count = 0
	if g.session['user']['accountType'] == 'student':
		for sess in g.session['user']['session']:
			if 'session_count' in sess:
				session_count += sess['session_count']
		if session_count >= g.session['user']['total_sessions']:
			return redirect(url_for('dashboard.plans', session_count=str(session_count), renew=True))	

	next_session = None
	sess_count = 0
	sessions = []
	if 'session' in g.session['user']:
		today = g.convert_to_local(datetime.now()).strftime("%A")
		current_time = g.from_server_time(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).time()
		users = []
		if g.session['user']['accountType'] == 'student':
			users = g.mongo.db.alquranlearningcenter.users.find({'accountType': 'teacher'})
		else:
			users = g.mongo.db.alquranlearningcenter.users.find({'accountType': 'student'})
		for session in g.session['user']['session']:
			for user in users:
				if user['email'] != g.session['user']['email']:
					if 'session' in user:
						for ss in user['session']:
							if ss['session_id'] == session['session_id']:
								s = ss.copy()
								tstart = s['time_start']
								s['time_start'] = g.convert_time(s['time_start'])
								tend = s['time_end']
								s['time_end'] = g.convert_time(s['time_end'])
								s['fname'] = user['fname']
								s['lname'] = user['lname']
								s['email'] = user['email']
								sessions.append(s)
								#print s['day']
								#print today
								if s['day'] == today:
									#try:
									#	time_start = datetime.strptime(session['time_start'], '%H:%M %p').time()
									#	time_end = datetime.strptime(session['time_end'], '%H:%M %p').time()
									#except:
									time_start = g.to_server_time(tstart).time()
									time_end = g.to_server_time(tend).time()
										
									#print current_time
									#print time_start
									#print time_end
									if current_time >= time_start and current_time <= time_end:
										next_session = s.copy()
										if sess_count >= 1:
											next_session['lname'] = next_session['lname'] + ' +'+str(sess_count)+' more'
										sess_count += 1
	#print sessions	
	return render_template('template.html', page='dashboard.html', current_user=g.session['user'], next_session=next_session, sessions=sessions, session_count=g.session['user']['session_count'])



@dashboard.route('/plans')
def plans():
	current_user = None
	email = ''
	renew = False
	session_count = 0
	payal_api_key = ''
	if g.isLoggedIn():
		paypal_api_key = gateway.client_token.generate()
		current_user = g.session['user']
		email = g.session['user']['email']
	if 'renew' in request.args:
		session_count = request.args.get('session_count')
		renew = True
	return render_template('template.html', page='plans.html', session_count=session_count,  current_user=current_user, email=email, renew=renew, paypal_api_key=paypal_api_key)


@dashboard.route('/checkout/<plan>')
def checkout(plan):
	print plan
	g.session['checkout'] = {
		'plan': plan
	}
	print g.session['checkout']
	return g.session['checkout']['plan']


def get_num_sessions(option):
	sessions = 0
	if option == 'Plan C' or option == 'Plan D' or option == 'Plan E' or option == 'Plan F':
		sessions = 8
	elif option == 'Plan A' or option == 'Plan B':
		sessions = 16
	elif option == 'Test':
		sessions = 4
	return sessions


@dashboard.route('/payment/<email>', methods=['GET', 'POST'])
def payment(email):
	if request.method == 'POST':
		status = request.form['payment_status']
		if status == 'Completed':
			#session = []
			#if 'session' in g.session['user']:
			#	session = g.session['user']['session']
			#g.mongo.db.alquranlearningcenter.users.update_one({'email': email}, {'$set': {
			#	'plan': request.form['option_selection1'],
			#	'last_paid': datetime.now().strftime("%m %d %Y"),
			#	'total_sessions': get_num_sessions(request.form['option_selection1']),
			#	'session': session
			#}})
			#payment_successful_email([request.form['payer_email'], 'syedakfatima1@gmail.com', 'admin@alquranlearningcenter.com'], request)
			return '200'
	return '400'
	



def payment_successful_email(to, fname, lname, plan, date):
	g.send_email(to, 'A.L.C. Payment Successful', '''                     
Hello,<br><br>
This is to confirm that you, '''+fname+' '+lname+''', has paid for '''+plan+''' starting '''+date+'''.<br><br>
You will receive an email soon confirming your attendance.
<br><br>
Thank You,
A.L.C.
        ''')



@dashboard.route('/complete')
def complete():
	if g.isLoggedIn() is False:
                return redirect(url_for('landing_page.index'))
	if 'paypal' not in request.referrer or 'checkout' not in g.session:
		return redirect(url_for('dashboard.plans'))
	session = []
	if 'session' in g.session['user']:
		session = g.session['user']['session']
	date = datetime.now().strftime("%m %d %Y")
	g.mongo.db.alquranlearningcenter.users.update_one({'email': g.session['user']['email']}, {'$set': {
		'plan': g.session['checkout']['plan'],
		'last_paid': date,
		'session_count': 1,
		'total_sessions': get_num_sessions(g.session['checkout']['plan']),
		'session': session
	}})
	payment_successful_email([g.session['user']['email'], 'syedakfatima1@gmail.com', 'admin@alquranlearningcenter.com'], g.session['user']['fname'], g.session['user']['lname'], g.session['checkout']['plan'], date.replace(' ', '/'))	
	return render_template('template.html', page='complete.html', current_user=g.session['user'])


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


@dashboard.route('/call/<session_id>')
def call(session_id):
	if g.isLoggedIn() is False:
		return redirect(url_for('landing_page.index'))
	for session in g.session['user']['session']:
		if session_id == session['session_id']:
			update = False
			current_date = datetime.now().strftime("%m/%d/%Y")
			if 'last_session' in session:
				if session['last_session'] != current_date:
					update = True
			else:
				update = True

			if update:
				g.mongo.db.alquranlearningcenter.users.update_one({
					"email": g.session['user']['email'],
					"session.session_id": session_id
				}, {"$set": {"session.$.last_session": current_date}})
				g.mongo.db.alquranlearningcenter.users.update_one({"email": g.session['user']['email']}, {"$inc": {"session_count": 1}})
	
	api_key = '45966672'	
	token = g.generate_token(session_id)
	
	if g.session['user']['accountType'] == 'teacher':
		return render_template('template.html', page='call_teacher.html', current_user=g.session['user'], session_id=session_id, token=token, api_key=api_key)
	elif g.session['user']['accountType'] == 'student':
		return render_template('template.html', page='call_student.html', current_user=g.session['user'], session_id=session_id, token=token, api_key=api_key)








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
