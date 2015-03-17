from flask import jsonify

def make_json_message(status: str, message: str, **kwargs) -> 'json':
	message = {'status': status, 'message': message}
	message.update(kwargs)
	return jsonify(message)