from flask import Blueprint, request, render_template, url_for, redirect
from web.blueprints import g

call = Blueprint('call', __name__, url_prefix='/call', template_folder='../templates', static_folder='../static')


@call.route('/<session_id>')
def session(session_id):

    exists = False
    token = ''
    session_secret = ''

    for sss in g.session['user']['session']:
        if sss['session_id'] is session_id:
            if 'session_secret' in sss:
                session_secret = sss['session_secret']
                token = sss['token']
                exists = True
                break

    if exists:
        return render_template('call.html', api_key='45966672', session_id=session_secret, token=token)
    return g.error_msg('failed to connect -> session_id: '+session_secret)
