from blueprints import g
import random
import string


class User:

    def __init__(self):
        self.obj = {}

    @staticmethod
    def generate_random(n=8):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    @staticmethod
    def get(uid):
        pass

    @staticmethod
    def is_anonymous():
        return False

    @staticmethod
    def user_to_dict(user):
        pass

    def authenticate(self):
        user = g.mongo.db.linx.users.find_one({"username": self.obj['username']})
        if user is not None:
            if g.bcrypt.check_password_hash(user["password"], self.obj['password']):
                if user['is_confirmed']:
                    if user['is_suspended'] is False:
                        return g.success_msg(User.user_to_dict(user))
                    return g.error_msg('your account has been suspended')
                return g.error_msg('a confirmation email has been sent to ' + user['email'])
        return g.error_msg('username or password incorrect')
