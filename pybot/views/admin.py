from pybot import app

from flask import render_template, request
from flask.ext.login import login_required
from wtforms import Form, StringField, SelectField, validators

forms = {}

class PybotForm(Form):
	def add_to_form(self, key):
		forms[key] = self 

class LinkForm(PybotForm):
	link_text = StringField('Text')
	# update to use only selectable endpoints
	endpoints = app.view_functions.keys()
	choices = [(e, e) for e in endpoints]
	url = SelectField('Link', choices=choices)

	@staticmethod
	def to_form():
		super().add_to_form('add_link')

@app.route('/admin/<section>')
@login_required
def admin(section=None):
	if section:
		form = forms.get(section)(request.form)
	return render_template('admin.html', form=form)