from . import app, HYPE_BUS
from flask import request

@app.route('/')
def index():
    return 'hello world'

@app.route('/echo')
def echo():
    if
