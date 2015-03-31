from collections import namedtuple

from pybot import app, login_manager
from pybot.db import dbhelpers

from flask import jsonify
from slugify import UniqueSlugify
import mistune

_slugify = UniqueSlugify(to_lower=True)
result_tuple = namedtuple('Result', ('status', 'message'))

# shortcuts to send response messages

def make_json_message(status: str, message: str, **kwargs) -> 'json':
	message = {'status': status, 'message': message}
	message.update(kwargs)
	return jsonify(message)

def get_result_message(pred: bool, success_msg: str, failure_msg: str,
					success_status='success', failure_status='error') -> result_tuple:
	if pred:
		return result_tuple(success_status, success_msg)
	else:
		return result_tuple(failure_status, failure_msg)

def form_error_message(form):
	return make_json_message('error', 'invalid form data', errors=form.errors)

# view decoratos

def linkable(func):
	try:
		app.config['LINKABLE_ENDPOINTS'].append(func.__qualname__)
	except KeyError:
		app.config['LINKABLE_ENDPOINTS'] = [func.__qualname__]
	return func

def login_view(func):
	login_manager.login_view = func.__qualname__
	return func

def slugify(title: str) -> str:
	if len(_slugify.uids) is 0:
		_slugify.uids = set(dbhelpers.get_page_slugs())
	return _slugify(title)

def htmlify(text: str):
	return mistune.markdown(text)
