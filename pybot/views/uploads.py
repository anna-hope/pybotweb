from pathlib import Path
from urllib.request import pathname2url

from pybot import app, helpers

from flask import (request, render_template, url_for, redirect,
				   jsonify, send_from_directory)
from werkzeug import secure_filename
from flask.ext.login import login_required, current_user
from wtforms import Form, FileField

class UploadForm(Form):
	image = FileField('image')

UPLOAD_PATH = app.config['UPLOAD_PATH']

@app.route('/upload_file/', methods=('GET', 'POST'))
@login_required
def upload_file():
	if request.method == 'POST' and 'image' in request.files:
		file = request.files['image']
		filename = secure_filename(file.filename)
		file_path = Path(app.name, app.config['UPLOAD_PATH'], filename)
		try:
			file.save(str(file_path))
		except FileNotFoundError:
			file_path.parent.mkdir(parents=True)
			file.save(str(file_path))
		new_file_url = request.url_root + pathname2url(str(Path(UPLOAD_PATH,
																filename)))
		return helpers.make_json_message('success', 'file upload succeeded',
										 url=new_file_url)
	form = UploadForm(request.form)
	if request.args.get('asjson'):
		return jsonify({field.name: field.__html__() for field in form})
	else:
		return render_template('uploads.html', form=form)

@app.route('/get_file/<filename>')
def serve_file(filename):
	file_path = Path(app.config['UPLOAD_PATH'], filename)
	# permanently redirect it to the static url
	return redirect(url_for('static', filename=str(file_path)), code=303)
