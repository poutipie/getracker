import time
from datetime import datetime
from dataclasses import dataclass
import requests
from typing import List
import os
import json

from getrecked import app
from flask import jsonify, render_template, request, send_from_directory

from .commons import Commons
from .db.database import Database
from .db.schema.item import Item
from .db.schema.volume import Volume
from .wiki_endpoint import WikiEndpoint


@app.route('/')
def root():
    return render_template("index.html")