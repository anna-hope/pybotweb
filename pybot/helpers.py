import functools

from pybot import app

from flask import jsonify

def make_json_message(status: str, message: str, **kwargs) -> 'json':
	message = {'status': status, 'message': message}
	message.update(kwargs)
	return jsonify(message)

def linkable(func):
	try:
		app.config['LINKABLE_ENDPOINTS'].append(func.__qualname__)
	except KeyError:
		app.config['LINKABLE_ENDPOINTS'] = []
		app.config['LINKABLE_ENDPOINTS'].append(func.__qualname__)
	return func