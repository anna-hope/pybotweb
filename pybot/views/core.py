from pybot import app, login_manager
from pybot.db import dbhelpers

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_required, login_user

@app.route('/')
def home():
	return render_template('index.html',
		header_message='pybot', 
		content='welcome to pybot',
		footer_message='pybot!')


@app.route('/login/', methods=('GET', 'POST'))
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email = request.form['email']
		password = request.form.get('password', None)
		if check_user(email, password):
			user = load_user(email)
			login_user(user)
			flash('Hi, {}!'.format(user.first_name))
	return redirect(url_for('home'))

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))


def check_user(email, password):
	user = dbhelpers.get_user(email=email)
	try:
		return user.password == password
	except AttributeError:
		return False

@login_manager.user_loader
def load_user(userid):
	# here, the userid is the user's email
	return dbhelpers.get_user(email=userid)


@app.route('/page/<page>')
def fetch_page(page=None):
	...