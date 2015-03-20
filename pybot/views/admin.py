from pybot import app
from pybot.db import dbhelpers

from flask import render_template, request, url_for
from flask.ext.login import login_required
from wtforms import Form, StringField, SelectField, validators

forms = {}

class PybotForm(Form):
	pass

class LinkForm(PybotForm):
	link_text = StringField('Text', (validators.InputRequired(), 
		validators.Length(max=20)))
	# update to use only selectable endpoints
	endpoints = app.view_functions.keys()
	choices = [(e, e) for e in endpoints]
	url = SelectField('Link', choices=choices)
	variable = StringField('Subpage')

	# hacky way of adding it to forms
	forms['links'] = __qualname__


@app.route('/admin/')
@app.route('/admin/<section>')
@login_required
def admin(section=None):
	forms_dict = {key: eval(value) for key, value in forms.items()}
	return render_template('admin.html', forms=forms_dict)

@app.route('/add_link/', methods=('POST',))
@login_required
def add_link():
	link_form = LinkForm(request.form)
	if request.method == 'POST' and link_form.validate():
		link_text = link_form.link_text.data
		url = link_form.url.data
		variable = link_form.variable.data
		dbhelpers.add_link(link_text, url, variable)
	return render_template(url_for('admin'))