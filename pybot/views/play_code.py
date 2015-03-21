from pybot import app, helpers
from flask import render_template

@app.route('/play/')
@helpers.linkable
def play():
	return render_template('play.html')