from pybot import app, login_manager
from pybot import helpers
from pybot.db import dbhelpers

from flask import (render_template, request, redirect, 
					url_for, flash, abort)
from flask.ext.login import login_required, login_user, logout_user, current_user
from wtforms import Form, TextField, PasswordField, validators

@app.route('/')
def home():
	return render_template('index.html',
		content='welcome to pybot')

class LoginForm(Form):
	email = TextField('email', (validators.InputRequired(), validators.Email()))
	password = PasswordField('password', (validators.InputRequired(),))

class RegistrationForm(Form):
	email = TextField('email', (validators.InputRequired(), validators.Email()))
	first_name = TextField('first name')
	surname = TextField('surname')
	password = PasswordField('password', (validators.InputRequired(),
										  validators.EqualTo('confirm_password',
										  	message='passwords must match')))
	confirm_password = PasswordField('and again')



@app.route('/login/', methods=('GET', 'POST'))
@helpers.login_view
def login():
	if current_user.is_authenticated():
		return redirect(url_for('home'))

	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		email = form.email.data
		password = form.password.data
		if check_user(email, password):
			user = load_user(email)
			login_user(user)
			flash('Hi, {}!'.format(user.first_name))
			if request.args.get('asjson'):
				return helpers.make_json_message('success', 
									'Hi, {}'.format(user.first_name))
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
		return user.check_password(password)
	except AttributeError:
		return False

@login_manager.user_loader
def load_user(userid: 'user email'):
	return dbhelpers.get_user(email=userid)

@app.route('/register/', methods=('GET', 'POST'))
def register_user():
	token = request.args.get('token', '')
	if not dbhelpers.check_token(token):
		return abort(403)
	
	form = RegistrationForm(request.form)
	if request.method == 'GET':
		return render_template('register.html', token=token, form=form)
	else:
		if form.validate():
			email = form.email.data
			password = form.password.data
			first_name = form.first_name.data
			surname = form.surname.data
			new_user = dbhelpers.create_user(
								  email=email, password=password, 
								  first_name=first_name, last_name=surname,
								  token=token)
			login_user(new_user)
			flash('Hi, {}!'.format(new_user.first_name))
			return helpers.make_json_message(
					'success', '{} was registered'.format(new_user))
		else:
			return helpers.form_error_message(form.errors)



