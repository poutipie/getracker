from flask import Flask

app = Flask(__name__)

from .getrecked import root
from .api import api