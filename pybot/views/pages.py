from urllib.parse import urljoin

from pybot import app
from pybot import helpers
from pybot.db import dbhelpers

from flask import render_template, jsonify, request, url_for, redirect
from wtforms import Form, StringField, TextAreaField, SelectField, validators
from flask.ext.login import login_required

import mistune

class NewPageForm(Form):
	page_title = StringField('title', (validators.required(), 
										validators.length(max=50)))
	page_category = SelectField('category', choices=[('none', 'uncategorized'), ('new', 'new')])
	new_page_category = StringField('new category', (validators.length(max=50),))
	new_page_content = TextAreaField('content (markdown)', (validators.required(),))


def create_page(title: str, content_markdown: str, category=None):
	if not category:
		category = app.config['DEFAULT_CATEGORY_NAME']
	slug = helpers.slugify(title)
	content_html = mistune.markdown(content_markdown)

	new_page = dbhelpers.create_new_page(title, slug, content_markdown, 
										content_html, category)
	return new_page

def modify_page(slug: str, title: str, content_markdown: str, category=None):
	content_html = mistune.markdown(content_markdown)
	dbhelpers.modify_page(slug, title=title, content_markdown=content_markdown,
											 content_html=content_html)


def get_page(slug: str):
	return dbhelpers.get_page(slug=slug)

def delete_page(slug: str):
	dbhelpers.delete_page(slug)

def get_category(slug: str):
	return dbhelpers.get_page_category(slug)

def get_categories():
	return dbhelpers.get_all_page_categories()

@app.route('/pages/')
@app.route('/pages/<slug>/')
@helpers.linkable
def render_page(slug=None):
	if slug:
		slug = slug.casefold()
		page = get_page(slug)
		if page:
			if request.args.get('asjson'):
				return jsonify({'title': page.title,
								'slug': page.slug,
								'content_markdown': page.content_markdown,
								'content_html': page.content_html})
			else:
				return render_template('pages.html', page=page, mode='page')
		else:

			# try finding a page category
			category = get_category(slug)
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
	return 'not implemented'

@app.route('/pages/add_new/', methods=('GET', 'POST'))
@login_required
def add_new_page():
	if request.method == 'GET':
		new_page_form = NewPageForm()
		new_page_form.page_category.choices += [set([(c.slug, c.title) for c in get_categories()])]
		return render_template('pages.html', mode='new_page', form=new_page_form)

	else:
		new_page_form = NewPageForm(request.form)
		new_page_form.page_category.choices += [(c.slug, c.title) for c in get_categories()]

		if new_page_form.validate():
			title = new_page_form.page_title.data
			content = new_page_form.new_page_content.data
			category = new_page_form.page_category.data

			if category == 'new':
				category = new_page_form.new_page_category.data
			elif category == 'none':
				category = None

			new_page = create_page(title, content, category)

			if request.args.get('asjson'):
				return helpers.make_json_message(
					'success', 'page {} was added'.format(title),
					**new_page)
			return redirect(urljoin(url_for('render_page'), new_page.get('slug', '')))

		else:
			return helpers.make_json_message(
				'error', new_page_form.errors)

@app.route('/pages/preview/', methods=('POST',))
@login_required
def preview_page():
	title = request.form.get('page_title', '')
	content_markdown = request.form.get('new_page_content', '')
	content_html = mistune.markdown(content_markdown)

	preview = {'title': title, 'content': content_html}
	return jsonify(preview)

@app.route('/pages/edit/', methods=('POST',))
@login_required
def edit_page():
	try:
		slug = request.form['slug']
	except KeyError:
		return helpers.make_json_message(
				'failure', 'you must provide a slug')
	new_title = request.form.get('title')
	content_markdown = request.form.get('new_page_content')
	modify_page(slug, new_title, content_markdown)
	return helpers.make_json_message(
				'success', 'page "{}" modified'.format(new_title))
	

@app.route('/pages/remove/', methods=('POST',))
@login_required
def remove_page():
	try:
		slug = request.form['slug']
	except KeyError:
		return helpers.make_json_message(
				'failure', 'you must provide a slug')
	delete_page(slug)
	return helpers.make_json_message(
			'success', 'page "{}" was deleted'.format(slug))