#!/usr/bin/env python3.4

import pathlib, asyncio

from pybot import app, load_app
import click, coffeescript

@asyncio.coroutine
def coffee_to_js(coffeefile_path, js_file_path):
    print('compiling {}'.format(coffeefile_path.name))
    loop = asyncio.get_event_loop()
    with coffeefile_path.open() as file:
        js_code = yield from loop.run_in_executor(None,
            coffeescript.compile, file.read())
    with js_file_path.open('w') as outputfile:
        outputfile.write(js_code)

@asyncio.coroutine
def compile_coffee(coffee_path='scripts', output_path=('static', 'scripts')):
    path = pathlib.Path(app.root_path, coffee_path)
    out_path = pathlib.Path(app.root_path, *output_path)
    if not out_path.exists():
        out_path.mkdir()

    to_compile = []

    for file in path.iterdir():
        if file.suffix == ('.coffee'):
            out_file = pathlib.Path(out_path, (file.stem + '.js'))
            to_compile.append(coffee_to_js(file, out_file))

    yield from asyncio.wait(to_compile)

def prepare_app(debug=False):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(compile_coffee())
    load_app()
    if debug:
        app.config.from_object('config.DebugConfig')
    else:
        app.config.from_object('config.ProductionConfig')


def run_production(host, port):
    prepare_app()
    # fix to use a production server
    app.run(host=host, port=port)

def run_debug(host, port, straightcoffee=False):
    app.config.from_object('config.DebugConfig')
    load_app()

    if straightcoffee:
        app.config['STRAIGHTCOFFEE'] = True
        # code to run coffeescript straight
        ...
    else:
        # compile coffeescript
        prepare_app(debug=True)

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