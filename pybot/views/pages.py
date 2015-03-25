from pybot import app
from pybot.db import dbhelpers

from flask import render_template, jsonify


def get_page(slug: str):
	return dbhelpers.get_page(slug)

def get_category(slug: str):
	return dbhelpers.get_page_category(slug)

def get_categories():
	return dbhelpers.get_all_page_categories():

@app.route('/pages/')
@app.route('/pages/<slug>/')
@linkable
def render_page(slug=None):
	if slug:
		page = get_page(slug)
		if page:
			return render_template('pages.html', page=page, category=False)
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
				return render_template('pages.html', page=(category,), category=True)
	else:
		return render_template('pages.html', page=dbhelpers.get_categories(),
								 category=True)

@app.route('/pages/<category>/<slug>/')
def render_subpage(category, slug):
	...