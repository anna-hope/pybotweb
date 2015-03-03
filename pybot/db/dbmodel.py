from pybot import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	_password = db.Column(db.String(255))

	def __init__(self, email, first_name, last_name):
		self.email = email.casefold()
		self.username = email.casefold()
		self.first_name = first_name
		self.last_name = last_name

	def __repr__(self):
		return 'User {} {}, {}'.format(
				self.first_name, self.last_name, self.email)

	def get_id(self):
		return self.email

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	@property
	def password(self):
	    return self._password
	@password.setter
	def password(self, value):
		# add code to test for complexity
	    self._password = value
	
	

class Page(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	content = db.Column(db.Text)

	def __init__(self):
		self.title = title
		self.content = content

	def __repr__(self):
		return 'Page {}'.format(self.title)