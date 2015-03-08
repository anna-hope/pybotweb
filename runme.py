#!/usr/bin/env python3.4

import pathlib

from pybot import app, load_app
import click, coffeescript


def compile_coffee(coffee_path='scripts', output_path=('static', 'scripts')):
    path = pathlib.Path(app.root_path, coffee_path)
    out_path = pathlib.Path(app.root_path, *output_path)
    if not out_path.exists():
        out_path.mkdir()

    for file in path.iterdir():
        if file.suffix == ('.coffee'):
            out_file = pathlib.Path(out_path, (file.stem + '.js'))

            with file.open() as coffeefile:
                js_text = coffeescript.compile(coffeefile.read())
            with out_file.open('w') as outfile:
                outfile.write(js_text)

def run_production(host, port):
    load_app()
    # fix to use a production server
    app.run(host=host, port=port)

def run_debug(host, port, straightcoffee=False):
    load_app()
    app.config.from_object('config.DebugConfig')

    if straightcoffee:
        app.config['STRAIGHTCOFFEE'] = True
        # code to run coffeescript straight
        ...
    else:
        # compile coffeescript
        compile_coffee()

    app.run(debug=True, host=host, port=port)

@click.command()
@click.option('--host', default='localhost', help='host')
@click.option('--port', default=8000, help='port')
@click.option('--debug', is_flag=True)
@click.option('--straightcoffee', is_flag=True)
def run(host, port, debug, straightcoffee):
    if debug:
        run_debug(host, port, straightcoffee)
    else:
        run_production(host, port)

if __name__ == '__main__':
    run()