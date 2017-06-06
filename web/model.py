import MySQLdb
import random
import string


def get_db():
    return MySQLdb.connect(host="localhost", user="root",  passwd="$Mdni00007", db="alquranlearningcenter")


def generate_random(n=8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def model_to_dict(raw, obj):
	attr = obj.__dict__
	count = 1
	for key, val in attr.iteritems():
		if key is not 'id':
			attr[key] = raw[count]
			count += 1
	return attr



class Session:

	def __init__(self, sid=None, uid_teacher=None, uid_student=None, datetime=None, duration=None, created=None, is_enabled=None):
		self.sid = sid
		self.uid_teacher = uid_teacher
		self.uid_student = uid_student
		self.datetime = datetime
		self.duration = duration
		self.created = created
		self.is_enabled = is_enabled

	@staticmethod
	def model_to_dict(raw):
		session = Session()
		session.sid = raw[1]
		session.uid_teacher = raw[2]
		session.uid_student = raw[3]
		session.datetime = raw[4]
		session.duration = raw[5]
		session.created = raw[6]
		session.is_enabled = raw[7]
		return vars(session)


	def get_from_id(self, multiple=False, get_all=False):
		db = get_db()
		cur = db.cursor()
		sql = 'SELECT * FROM sessions'
		if not get_all: 
			if self.sid is not None:
				cur.execute(sql+' WHERE sid=%s AND is_enabled=%s', (self.sid, 'true'))
			elif self.uid_teacher is not None:
				cur.execute(sql+' WHERE uid_teacher=%s AND is_enabled=%s', (self.uid_teacher, 'true'))
			elif self.uid_student is not None:
				cur.execute(sql+' WHERE uid_student=%s AND is_enabled=%s', (self.uid_student, 'true'))
			else:
				return None
			if multiple:
				raws = cur.fetchall()
				not_raw = []
				for raw in raws:
					not_raw.append(Session.model_to_dict(raw))
				return not_raw
			else:
				raw = cur.fetchone()
				return None if raw is None else Session.model_to_dict(raw)
		else:
			cur.execute(sql)
			raws = cur.fetchall()
			not_raw = []
			for raw in raws:
				not_raw.append(Session.model_to_dict(raw))
			return not_raw

