from flask import Blueprint, request, render_template, url_for, redirect
from web.blueprints import g
from opentok import OpenTok


admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../templates', static_folder='../static')


API_KEY = '45966672'
API_SECRET = '728a640798d19162ed49d02ebd5a6153446b8421'

opentok = OpenTok(API_KEY, API_SECRET)


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

        s = opentok.create_session()
        id = s.session_id
        token = opentok.generate_token(id)


        g.mongo.db.alquranlearningcenter.users.update_one({"email": teacher}, {'$push': {"session": {
            "session_id": id,
            "token": token,
            "day": day,
            "time_start": time_start,
            "time_end": time_end
        }}})

        g.mongo.db.alquranlearningcenter.users.update_one({"email": student}, {'$push': {"session": {
            "session_id": id,
            "token": token,
            "day": day,
            "time_start": time_start,
            "time_end": time_end
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
        session_id = request.form['session_id']

        g.mongo.db.alquranlearningcenter.users.update_one({"email": email}, {'$pull': {"session": {"session_id": session_id}}})

        return g.success_msg({"email": email})




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
