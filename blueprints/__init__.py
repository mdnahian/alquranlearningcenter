import json


class g:
    def __init__(self):
        self.mongo = None
        self.bcrypt = None
        self.login_manager = None
        self.socketio = None
        self.current_user = None

    @staticmethod
    def error_msg(msg):
        return '{"status": "error", "message": "' + msg + '"}'

    @staticmethod
    def success_msg(response):
        return '{"status": "success", "response": ' + json.dumps(response) + '}'
