from enum import IntEnum

from pybot import app
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	_password_hash = db.Column(db.String(255))

	def __init__(self, email: str, first_name: str, last_name: str,
					password=''):
		self.email = email
		self.username = email
		self.first_name = first_name
		self.last_name = last_name
		self.password = password


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
		# this is not meant to be used directly
	    return self._password_hash
	@password.setter
	def password(self, value):
	    self._password_hash = generate_password_hash(value)

	def check_password(self, password: str):
		return check_password_hash(self.password, password)
	
class RegistrationToken(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	token = db.Column(db.String(100), unique=True)

	def __init__(self, token: str):
		self.token = token

	def __repr__(self):
		return 'Registration Token {}'.format(self.token)

class Page(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), unique=True)
	content_markdown = db.Column(db.Text)
	content_html = db.Column(db.Text)
	slug = db.Column(db.String(100), unique=True)

	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category = db.relationship('Category', backref=db.backref('pages', lazy='dynamic'))

	def __init__(self, title: str, slug: str,
					content_markdown: str, content_html: str,
					category):
		self.title = title
		self.content_markdown = content_markdown
		self.content_html = content_html
		self.slug = slug
		self.category = category

	def __repr__(self):
		return 'Page {}'.format(self.title)

class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text(50), unique=True)
	slug = db.Column(db.Text(50), unique=True)

	def __init__(self, title: str, slug: str):
		self.title = title
		self.slug = slug

	def __repr__(self):
		return 'Page Category {}'.format(self.title)


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