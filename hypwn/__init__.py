from flask import Flask

app = Flask(__name__, static_url_path='/static', static_folder='frontend/dist')

from . import bus

# global bus
HYPE_BUS = bus.Hype()

from . import api, views
