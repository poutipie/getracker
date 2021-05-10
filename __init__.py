from flask import Flask

app = Flask(__name__)

# The connection points use circular dependency to app
from .getrecked import root
from .journal import journal
from .api import api
