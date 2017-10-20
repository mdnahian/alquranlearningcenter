from flask import Blueprint, request, render_template, url_for, redirect
from web.blueprints import g
from bson.objectid import ObjectId

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../templates', static_folder='../static')


def check_admin():
    if g.session['user']['accountType'] != 'admin':
        return redirect(url_for('dashboard.web'))



@admin.route('/session', methods=['POST'])
def session():
    check_admin()
    if request.method == 'POST':
        teacher = request.form['teacher']
        student = request.form['student']
        day = request.form['day']
        time_start = request.form['time_start']
        time_end = request.form['time_end']
	sid = g.generate_random()
	
	s = g.mongo.db.alquranlearningcenter.users.find_one({'email': student})
	if 'total_sessions' not in s or 'last_paid' not in s or g.check_date(s['last_paid']) == False:
		g.mongo.db.alquranlearningcenter.users.update_one({'email': student}, {'$set': {
			'total_sessions': 2,
			'session_count': 1,
			'last_paid': datetime.now().strftime("%m %d %Y"),
			'plan': 'Test'
		}})	

	id = ''

	t = g.mongo.db.alquranlearningcenter.users.find_one({'email': teacher})
	if 'session_id' not in t:
        	s = opentok.create_session()
        	id = s.session_id
		g.mongo.db.alquranlearningcenter.users.update_one({'email': teacher}, {'$set': {'session_id': id}})
	else:
		id = t['session_id']

	

        g.mongo.db.alquranlearningcenter.users.update_one({"email": teacher}, {'$push': {"session": {
            "session_id": id,
            "day": day,
            "time_start": time_start,
            "time_end": time_end,
            "sid": sid
        }}})

        g.mongo.db.alquranlearningcenter.users.update_one({"email": student}, {'$push': {"session": {
            "session_id": id,
            "day": day,
            "time_start": time_start,
            "time_end": time_end,
            "sid": sid
        }}})
	
	g.send_email([teacher, student], 'A.L.C. Schedule Update', '''
	Hello,<br><br>
	The following session has been added to your schedule:<br><br>
	Day: <strong>'''+day+'''</strong><br>
	Time Start: <strong>'''+g.convert_time(time_start)+'''</strong><br>
	Time End: <strong>'''+g.convert_time(time_end)+'''</strong><br>
	<br><br>
	Thank You,
	A.L.C. Team 
	''')

        #return g.success_msg({"teacher": teacher, "student": student})
	return redirect(url_for('admin.panel'))


@admin.route('/remove_session', methods=['POST'])
def remove_session():
    check_admin()
    if request.method == 'POST':
        email = request.form['email']
        sid = request.form['sid']
	
	users = g.mongo.db.alquranlearningcenter.users.find({})
	other_email = ''
	for user in users:
		if email != user['email']:
			if 'session' in user:
				for session in user['session']:
					if sid == session['sid']:
						other_email = user['email']
						break
		if other_email != '':
			break

        g.mongo.db.alquranlearningcenter.users.update_one({"email": email}, {'$pull': {"session": {"sid": sid}}})
	if other_email != '':
		g.mongo.db.alquranlearningcenter.users.update_one({"email": other_email}, {'$pull': {"session": {"sid": sid}}})
        return g.success_msg({"email": email})



@admin.route('/user/<email>')
def view_user(email):
    check_admin()
    user = dict(g.mongo.db.alquranlearningcenter.users.find_one({'email': email}))
    del user['confirm']
    del user['password']
    del user['confirmation_key']
    del user['_id']
    return render_template('template.html', page='user.html', current_user=g.session['user'], user=user)


@admin.route('/')
def panel():
    check_admin()
    teachers = list(g.mongo.db.alquranlearningcenter.users.find({"accountType": "teacher"}))
    students = list(g.mongo.db.alquranlearningcenter.users.find({"accountType": "student"}))

    for teacher in teachers:
        if 'session' not in teacher:
	    teacher['session'] = []
	else:	
		for session in teacher['session']:
			session['time_start'] = g.convert_time(session['time_start'])
			session['time_end'] = g.convert_time(session['time_end'])
    for student in students:
	student['paid'] = False
	if 'last_paid' in student:
            student['paid'] = g.check_date(student['last_paid'])
	    student['last_paid'] = student['last_paid'].replace(' ', '/')
	if 'session' not in student:
	    student['session'] = []
	else:	
		for session in student['session']:
                        session['time_start'] = g.convert_time(session['time_start'])
                        session['time_end'] = g.convert_time(session['time_end'])
    return render_template('template.html', page='admin.html', current_user=g.session['user'], teachers=teachers, students=students)
