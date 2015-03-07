from pybot import app
from flask import render_template

@app.route('/play/')
def play():
	return render_template('play.html')