from flask import Blueprint, request, render_template, url_for, redirect
from blueprints import g
import json


admin = Blueprint('dashboard', __name__, url_prefix='/admin', template_folder='../templates', static_folder='../static')


def check_admin():
	if g.session['user']['accountType'] == 'admin':
		pass
	else:
		return redirect(url_for('dashboard.web'))


@admin.route('/')
def admin():
	check_admin()
	return render_template('templates.html', page='admin.html', current_user=g.session['user'])
