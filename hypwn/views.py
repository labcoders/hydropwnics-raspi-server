from . import app, HYPE_BUS, redirect

@app.route('/')
def index():
    return redirect('/static/index.html')
