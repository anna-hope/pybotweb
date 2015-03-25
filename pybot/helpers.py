from pybot import app
from pybot.db import dbhelpers

from flask import jsonify
from slugify import Slugify

_slugify = UniqueSlugify()
_slugify.uids = set(dbhelpers.get_page_slugs())

def make_json_message(status: str, message: str, **kwargs) -> 'json':
	message = {'status': status, 'message': message}
	message.update(kwargs)
	return jsonify(message)

def linkable(func):
	try:
		app.config['LINKABLE_ENDPOINTS'].append(func.__qualname__)
	except KeyError:
		app.config['LINKABLE_ENDPOINTS'] = [func.__qualname__]
	return func

def slugify(title: str) -> str:
	return _slugify(title)