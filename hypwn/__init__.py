from flask import Flask

app = Flask(__name__)

from . import bus

# global bus
HYPE_BUS = bus.Hype()

from . import api
