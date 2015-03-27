from pybot import app
from pybot import helpers
from pybot.db import dbhelpers

from flask import render_template, jsonify, request
from wtforms import Form, StringField, TextAreaField, SelectField, validators
from flask.ext.login import login_required

class NewPageForm(Form):
	page_title = StringField('title', (validators.required(), 
										validators.length(max=50)))
	page_category = SelectField('category', choices=[('new', 'new')])
	new_page_category = StringField('new category', (validators.length(max=50),))
	new_page_content = TextAreaField('content (markdown)', (validators.required(),))


def get_page(slug: str):
	return dbhelpers.get_page(slug)

def get_category(slug: str):
	return dbhelpers.get_page_category(slug)

def get_categories():
	return dbhelpers.get_all_page_categories()

@app.route('/pages/')
@app.route('/pages/<slug>/')
@helpers.linkable
def render_page(slug=None):
	if slug:
		page = get_page(slug)
		if page:
			return render_template('pages.html', page=page, mode='page')
		else:

			# try finding a page category
			category = get_category(title)
			if request.args.get('asjson'):
				return jsonify({'title': category.title,
								'slug': category.slug,
								'subpages': [{'title': p.title,
											 'slug': p.slug}
											 for p in category.pages.all()]})
			else:
				return render_template('pages.html', page=(category,), mode='category')
	else:
		return render_template('pages.html', page=get_categories(),
								 mode='category')

@app.route('/pages/<category>/<slug>/')
def render_subpage(category, slug):
	...

@app.route('/pages/add_new/', methods=('GET', 'POST'))
@login_required
def add_new_page():
	if request.method == 'GET':
		new_page_form = NewPageForm()
		new_page_form.page_category.choices += [(c.slug, c.title) for c in get_categories()]
		return render_template('pages.html', mode='new_page', form=new_page_form)

	else:
		new_page_form = NewPageForm(request.post)
		new_page_form.page_category.choices += [(c.slug, c.title) for c in get_categories()]

		if new_page_form.validate():
			title = new_page_form.page_title.data
			content = new_page_form.new_page_content.data
			category = new_page_form.page_category.data

			if category == 'new':
				category = new_page_form.new_page_category.data

			dbhelpers.create_page(title, content, category)

			if request.args.get('asjson'):
				return helpers.make_json_message(
					'success', 'page {} was added'.format(title))
			return 'success'

		else:
			if request.args.get('asjson'):
				return helpers.make_json_message(
					'error', new_page_form.errors)
			return 'success'