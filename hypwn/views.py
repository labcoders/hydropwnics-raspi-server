from . import app, HYPE_BUS
from flask import redirect, send_from_directory

@app.route('/')
def index():
    return redirect('/static/index.html')

@app.route('/static/<p>')
def static(p):
    return send_from_directory(p)
