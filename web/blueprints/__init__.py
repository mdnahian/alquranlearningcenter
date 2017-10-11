import json
import random
import string
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sparkpost import SparkPost

sp = SparkPost('ad651ed0ecf1284a04e30b6c25fc97db8e3bc0e9')

class g:
    def __init__(self):
        self.mongo = None
        self.bcrypt = None
        self.session = None
        self.current_user = None

    @staticmethod
    def from_server_time(str_time):
        return datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S") - timedelta(hours=4)

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
        current_date = datetime.today() - relativedelta(days=2)
        last_paid = datetime.strptime(paid_date, "%m %d %Y")
        next_date = datetime.today() + relativedelta(months=1)

        print current_date
        print last_paid
        print next_date

        if last_paid >= current_date and last_paid < next_date:
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
    def isLoggedIn():
        g.sumSessionCounter()
        return 'user' in g.session

    @staticmethod
    def sumSessionCounter():
        try:
            g.session['counter'] += 1
        except KeyError:
            g.session['counter'] = 1
