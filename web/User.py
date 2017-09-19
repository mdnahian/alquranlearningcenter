from web.blueprints import g
import random
import string


class User:

    def __init__(self, email, password):
        self.obj = {
            "email": email,
            "password": password
        }

    @staticmethod
    def generate_random(n=8):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    def user_serializable(self):
        user = self.obj
        user['_id'] = False
        return user

    def authenticate(self):
        user = g.mongo.db.alquranlearningcenter.users.find_one({"email": self.obj['email']})
        if user is not None:
            if g.bcrypt.check_password_hash(user["password"], self.obj['password']):
                if user['isConfirmed']:
                    if user['isSuspended'] is False:
                        self.obj = user
                        return True, g.success_msg(self.user_serializable())
                    return False, g.error_msg('your account has been suspended')
                return False, g.error_msg('a confirmation email has been sent to ' + user['email'])
        return False, g.error_msg('email or password incorrect')
