from . import app, HYPE_BUS

from flask import request

@app.route('/')
def index():
    return 'hello world'

@app.route('/echo')
def echo():
    if request.method == 'POST':
        d = request.json
        b = d['value']
        b_ = HYPE_BUS.echo(b)
        return '{} echoed to {}'.format(b, b_)
