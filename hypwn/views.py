from . import app, HYPE_BUS, render_template, redirect

@app.route('/')
def index():
    return redirect('/static/index.html')
