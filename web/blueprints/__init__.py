import json
import random
import string
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import tz
from sparkpost import SparkPost
from opentok import OpenTok

sp = SparkPost('ad651ed0ecf1284a04e30b6c25fc97db8e3bc0e9')

API_KEY = '45966672'
API_SECRET = '728a640798d19162ed49d02ebd5a6153446b8421'

opentok = OpenTok(API_KEY, API_SECRET)


from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')

class g:
    def __init__(self):
        self.mongo = None
        self.bcrypt = None
        self.session = None
        self.current_user = None

    @staticmethod
    def convert_to_local(t):
	return t.replace(tzinfo=from_zone).astimezone(to_zone)

    @staticmethod
    def from_server_time(str_time):
        return g.convert_to_local(datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S"))

    @staticmethod
    def generate_token(session_id):
        return opentok.generate_token(session_id)    

    @staticmethod
    def send_email(emails, subject, body):
        response = sp.transmissions.send(
            use_sandbox=False,
            recipients=emails,
            html=body,
            from_email='hello@alquranlearningcenter.com',
            subject=subject
        )
        print response

    @staticmethod
    def to_server_time(str_time):
	return datetime.strptime(str_time, "%H:%M")

    @staticmethod
    def convert_time(str_time):
	return datetime.strptime(str_time, "%H:%M").strftime("%I:%M %p")

    @staticmethod
    def check_date(paid_date):
        current_date = g.convert_to_local(datetime.today())
        last_paid = g.convert_to_local(datetime.strptime(paid_date, "%m %d %Y"))
        next_date = current_date + relativedelta(months=1)

        #print current_date
        #print last_paid
        #print next_date

        if current_date >= last_paid and last_paid < next_date:
                return True
        return False
 

    @staticmethod
    def error_msg(msg):
        return '{"status": "error", "message": "' + msg + '"}'

    @staticmethod
    def generate_random(n=8):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    @staticmethod
    def success_msg(response):
        return '{"status": "success", "response": ' + json.dumps(response) + '}'

    @staticmethod
    def is_enabled():
        global_settings = g.mongo.db.alquranlearningcenter.settings.find_one({'type': 'global'})
        return global_settings['is_enabled']
                
    @staticmethod
    def isLoggedIn():	
        g.sumSessionCounter()
        return 'user' in g.session

    @staticmethod
    def sumSessionCounter():
        try:
            g.session['counter'] += 1
        except KeyError:
            g.session['counter'] = 1
