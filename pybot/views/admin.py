from collections import namedtuple

from pybot import app, helpers
from pybot.db import dbhelpers

from flask import render_template, request, url_for, redirect
from flask.ext.login import login_required
from wtforms import Form, StringField, SelectField, validators
from wtforms.validators import ValidationError

form_names = {}
form_tuple = namedtuple('PybotForm', ('form', 'name', 'endpoint', 'caption'))

class PybotForm(Form):
	pass

class LinkForm(PybotForm):
	link_text = StringField('Text', 
		(validators.InputRequired(message='please enter the text'), 
		validators.Length(max=20)))
	# update to use only selectable endpoints
	endpoint_choice = SelectField('Endpoint', (validators.InputRequired(),))
	variable = StringField('Subpage')

	# hacky way of adding it to forms
	form_names['add_link'] = __qualname__

class RemoveLinkForm(PybotForm):
	remove_link_choice = SelectField('Link', validators=(
			validators.InputRequired(message='please select a link'),))
	form_names['remove_link'] = __qualname__


class HeaderForm(PybotForm):
	new_header_text = StringField('Header', (validators.InputRequired(),
												validators.Length(min=5, max=10)))
	form_names['change_header'] = __qualname__

class FooterForm(PybotForm):
	new_footer_text = StringField('Footer')
	form_names['change_footer'] = __qualname__


captions = {
	'add_link': 'add a link',
	'remove_link': 'remove a link',
	'change_header': 'change the header',
	'change_footer': 'change the footer'
}


@app.route('/admin/')
@login_required
def admin(section=None):
	forms_dict = {key: eval(value)() for key, value in form_names.items()}

	# add choices to forms
	forms_dict['add_link'].endpoint_choice.choices = (
		(e, url_for(e)) for e in app.config['LINKABLE_ENDPOINTS'])
	forms_dict['remove_link'].remove_link_choice.choices = (
		(link.text, link.text) for link in dbhelpers.get_links())
	forms = (form_tuple(form, k, k, captions[k]) for k, form in sorted(forms_dict.items(), key=lambda i: i[0]))

	return render_template('admin.html', forms=forms)

@app.route('/add_link/', methods=('POST',))
@login_required
def add_link():
	link_form = LinkForm(request.form)
	link_form.endpoint_choice.choices = (
			(e, url_for(e)) for e in app.config['LINKABLE_ENDPOINTS'])
	if link_form.validate():
		link_text = link_form.link_text.data
		endpoint_choice = link_form.endpoint_choice.data
		variable = link_form.variable.data
		dbhelpers.add_link(link_text, endpoint_choice, variable)
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
	remove_link_form.remove_link_choice.choices = (
		(link.text, link.text) for link in dbhelpers.get_links())
	if remove_link_form.validate():
		link_text = remove_link_form.remove_link_choice.data
		result = dbhelpers.remove_link(link_text)
		message = helpers.get_result_message(result,
					success_msg='link {} was removed'.format(link_text),
					failure_msg='link {} could not be removed'.format(link_text))
		return helpers.make_json_message(message)
	else:
		return helpers.form_error_message(remove_link_form)

@app.route('/change_header/', methods=('POST',))
@login_required
def change_header():
	header_form = HeaderForm(request.form)
	if header_form.validate():
		header_text = helpers.htmlify(header_form.new_header_text.data)
		result = dbhelpers.set_header(header_text)
		message = helpers.get_result_message(result,
					success_msg='header updated to "{}"'.format(header_text),
					failure_msg='footer could not be updated')
		return helpers.make_json_message(*message)
	else:
		return helpers.form_error_message(header_form)

@app.route('/change_footer/', methods=('POST',))
@login_required
def change_footer():
	footer_form = FooterForm(request.form)
	if footer_form.validate():
		footer_text = helpers.htmlify(footer_form.new_footer_text.data)
		result =  dbhelpers.set_footer(footer_text)
		message = helpers.get_result_message(result, 
					success_msg='footer updated to "{}"'.format(footer_text), 
					failure_msg='footer could not be updated')
		return helpers.make_json_message(*message)
	else:
		return helpers.form_error_message(footer_form)