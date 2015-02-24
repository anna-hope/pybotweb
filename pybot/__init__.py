import pathlib, importlib

from flask import Flask

app = Flask('pybot')

def load_app():
	importlib.import_module('{}.views'.format(app.name))
	views = pathlib.Path(app.root_path, 'views')
	for file in views.iterdir():
		if file.suffix == '.py':
			importlib.import_module(name='.{}'.format(file.stem),
									package='{}.views'.format(app.name))


