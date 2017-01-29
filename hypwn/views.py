from . import app, HYPE_BUS
from flask import redirect

@app.route('/')
def index():
    return redirect('/static/index.html')
