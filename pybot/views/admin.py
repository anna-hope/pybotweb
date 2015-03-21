from pybot import app, helpers
from pybot.db import dbhelpers

from flask import render_template, request, url_for, redirect
from flask.ext.login import login_required
from wtforms import Form, StringField, SelectField, validators
from wtforms.validators import ValidationError

forms = {}

class PybotForm(Form):
	pass

class LinkForm(PybotForm):
	link_text = StringField('Text', 
		(validators.InputRequired(message='please enter the text'), 
		validators.Length(max=20)))
	# update to use only selectable endpoints
	url = SelectField('Link', (validators.InputRequired(),))
	variable = StringField('Subpage')

	# hacky way of adding it to forms
	forms['links'] = __qualname__

class RemoveLinkForm(PybotForm):
	link = SelectField('Link', validators=(
			validators.InputRequired(message='please select a link'),))
	forms['remove_links'] = __qualname__


@app.route('/admin/')
@app.route('/admin/<section>')
@login_required
def admin(section=None):
	forms_dict = {key: eval(value)() for key, value in forms.items()}

	# add choices to forms
	forms_dict['links'].url.choices = ((e, e) for e in app.config['LINKABLE_ENDPOINTS'])
	forms_dict['remove_links'].link.choices = ((link.text, link.text) for link in dbhelpers.get_links())

	return render_template('admin.html', forms=forms_dict)

@app.route('/add_link/', methods=('POST',))
@login_required
def add_link():
	link_form = LinkForm(request.form)
	link_form.url.choices = [(e, e) for e in app.config['LINKABLE_ENDPOINTS']]
	if link_form.validate():
		link_text = link_form.link_text.data
		url = link_form.url.data
		variable = link_form.variable.data
		dbhelpers.add_link(link_text, url, variable)
		if request.args.get('asjson'):
			return helpers.make_json_message('success', 
							'link {} was added successfully'.format(link_text))
	else:
		if request.args.get('asjson'):
			return helpers.make_json_message('error', 'invalid data')
	return redirect(url_for('admin'))

@app.route('/remove_link/', methods=('POST',))
@login_required
def remove_link():
	remove_link_form = RemoveLinkForm(request.form)
	remove_link_form.link.choices = ((link.text, link.text) for link in dbhelpers.get_links())
	if request.method == 'POST' and remove_link_form.validate():
		link_text = remove_link_form.link.data
		if dbhelpers.remove_link(link_text):
			status = 'success'
			message = 'link {} was removed'.format(link_text)
		else:
			status = 'error'
			message = 'link {} does not exist'.format(link_text)
	else:
		status = 'error'
		message = remove_link_form.errors

	if request.args.get('asjson'):
		return helpers.make_json_message(status, message)
	return redirect(url_for('admin'))



