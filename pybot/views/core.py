from pybot import app, login_manager
from pybot import helpers
from pybot.db import dbhelpers

from flask import (render_template, request, redirect, 
					url_for, flash)
from flask.ext.login import login_required, login_user, logout_user
from wtforms import Form, TextField, PasswordField, validators

@app.route('/')
def home():
	return render_template('index.html',
		content='welcome to pybot')

class LoginForm(Form):
	email = TextField('email', (validators.Email, validators.InputRequired))
	password = PasswordField('password', (validators.InputRequired,))


@app.route('/login/', methods=('GET', 'POST'))
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		email = form.email.data
		password = form.password.data
		if check_user(email, password):
			user = load_user(email)
			login_user(user)
			flash('Hi, {}!'.format(user.first_name))
			message = {'status': 'success', 'message': 'Hi, {}'.format(user.first_name)}
			if request.args.get('asjson'):
				return helpers.make_json_message(**message)
			return redirect(url_for('home'))
		else:
			error = 'The login data you provided did not work :('
			# move this to the strings file
			if request.args.get('asjson'):
				return helpers.make_json_message('error', error)
	return render_template('login.html', form=form, error=error)
	
@app.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))


def check_user(email, password) -> bool:
	user = dbhelpers.get_user(email=email)
	try:
		return user.password == password
	except AttributeError:
		return False

@login_manager.user_loader
def load_user(userid: 'user email') -> 'User':
	return dbhelpers.get_user(email=userid)


@app.route('/page/<page>')
def fetch_page(page=None):
	...