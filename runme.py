#!/usr/bin/env python3.4

from pybotweb import app
import click


def run_production(host, port):
    ...

def run_debug(host, port):
    app.run(host=host, port=port, debug=True)

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