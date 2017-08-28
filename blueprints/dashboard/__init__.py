from flask import Blueprint, request, render_template, url_for
from blueprints import g
import json


dashboard = Blueprint('dashboard', __name__, url_prefix='/web', template_folder='../templates', static_folder='../static')


@dashboard.route('/')
def web():
    return render_template('template.html', page='dashboard.html')
