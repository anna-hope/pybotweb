from pybot import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))

	def __init__(self, email, first_name, last_name):
		self.email = email
		self.username = email
		self.first_name = first_name
		self.last_name = last_name

	def __repr__(self):
		return 'User {} {}, {}'.format(
				self.first_name, self.last_name, self.email)

class Page(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	content = db.Column(db.Text)

	def __init__(self):
		self.title = title
		self.content = content

	def __repr__(self):
		return 'Page {}'.format(self.title)