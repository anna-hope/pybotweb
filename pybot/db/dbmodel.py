from enum import IntEnum

from pybot import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	_password = db.Column(db.String(255))

	def __init__(self, email: str, first_name: str, last_name: str):
		self.email = email.casefold()
		self.username = email.casefold()
		self.first_name = first_name
		self.last_name = last_name

	def __repr__(self):
		return 'User {} {}, {}'.format(
				self.first_name, self.last_name, self.email)

	def get_id(self):
		return self.email

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

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

	def __init__(self, title: str, content: str):
		self.title = title
		self.content = content

	def __repr__(self):
		return 'Page {}'.format(self.title)

class MessageType(IntEnum):
	header = 1
	footer = 2

class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	message_type = db.Column(db.Integer, unique=True)
	text = db.Column(db.Text)

	def __init__(self, message_type: MessageType, text: str):
		self.message_type = message_type
		self.text = text

	def __repr__(self):
		return '{}: {}'.format(self.message_type, self.text)

class Link(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	endpoint = db.Column(db.String(120))
	variable = db.Column(db.String(255))
	text = db.Column(db.String(255), unique=True)

	def __init__(self, text: str, endpoint='', variable=''):
		self.text = text
		self.endpoint = endpoint
		self.variable = variable

	def __repr__(self):
		return 'Link {}: {}/{}'.format(self.text, self.endpoint,
								 self.variable)