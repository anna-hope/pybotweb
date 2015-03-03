import pathlib, importlib

from flask.ext.login import LoginManager

from flask import Flask

app = Flask('pybot')
login_manager = LoginManager()

def load_app():
	login_manager.init_app(app)

	importlib.import_module('{}.views'.format(app.name))
	views = pathlib.Path(app.root_path, 'views')
	for file in views.iterdir():
		if file.suffix == '.py':
			importlib.import_module(name='.{}'.format(file.stem),
									package='{}.views'.format(app.name))


