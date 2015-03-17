from urllib.parse import urljoin

from pybot import app
from pybot.db import dbhelpers

from flask import url_for

@app.context_processor
def inject_header():
	try:
		header_text = dbhelpers.get_header().text
	except AttributeError:
		header_text = 'no header text set'
	return {'header_message': header_text}

@app.context_processor
def inject_footer():
	try:
		footer_text = dbhelpers.get_footer().text
	except AttributeError:
		footer_text = 'no footer text set'
	return {'footer_message': footer_text}

@app.context_processor
def inject_links():
	links = ({'text': link.text,
			 'url': urljoin(url_for(link.endpoint), link.variable)}
			 for link in dbhelpers.get_links())
	return {'links': links}