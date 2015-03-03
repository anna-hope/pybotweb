#!/usr/bin/env python3.4

from pybot import app, load_app
import click


def run_production(host, port):
    load_app()
    # fix to use a production server
    app.run(host=host, port=port)

def run_debug(host, port):
    load_app()
    app.config.from_object('config.DebugConfig')
    app.run(debug=True, host=host, port=port)

@click.command()
@click.option('--host', default='localhost', help='host')
@click.option('--port', default=8000, help='port')
@click.option('--debug', is_flag=True)
def run(host, port, debug):
    if debug:
        run_debug(host, port)
    else:
        run_production(host, port)

if __name__ == '__main__':
    run()