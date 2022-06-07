from flask import Flask

app = Flask(__name__)

# The connection points use circular dependency to app
from .getracker import root
from .api import api

from .db.databaseindexer import DatabaseIndexer

indexer = DatabaseIndexer()