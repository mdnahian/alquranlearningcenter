import MySQLdb
import random
import string


class User:

    def __init__(self, uid=None, fname=None, lname=None, email=None, password=None,
                 is_confirmed=None, age=None, languages=None, gender=None, proficiency=None,
                 availability=None, is_enabled=None, account_type=None):
        self.uid = uid
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.is_confirmed = is_confirmed
        self.age = age
        self.languages = languages
        self.gender = gender
        self.proficiency = proficiency
        self.availability = availability
        self.is_enabled = is_enabled
        self.account_type = account_type

    @staticmethod
    def get_db():
        return MySQLdb.connect(host="localhost", user="root",  passwd="$Mdni00007", db="users")

    @staticmethod
    def generate_random(n=8):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    def signup(self):
        db = self.get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (self.uid, self.fname, self.lname, self.email, self.password, self.age,
                     self.languages, self.gender, self.proficiency, self.availability, self.is_enabled, self.account_type))
        cur.commit()
        db.close()

    def db_to_user(self, raw_user):
        self.uid = raw_user[0]
        self.fname = raw_user[1]
        self.lname = raw_user[2]
        self.email = raw_user[3]
        self.password = raw_user[4]
        self.is_confirmed = raw_user[5]
        self.age = raw_user[6]
        self.languages = raw_user[7]
        self.gender = raw_user[8]
        self.proficiency = raw_user[9]
        self.availability = raw_user[11]
        self.is_enabled = raw_user[12]
        self.account_type = raw_user[13]
        return self

    def get(self, uid):
        db = self.get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE uid=?", (uid, ))
        raw_user = cur.fetchone()
        return self.db_to_user(raw_user) if raw_user is not None else raw_user

    def is_authenticated(self):
        db = self.get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (self.email, self.password))
        raw_user = cur.fetchone()
        if raw_user is not None:
            self.db_to_user(raw_user)
            return True
        return False

    def is_active(self):
        return self.is_enabled is 'true'

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.uid









