from getrecked import app
from flask import jsonify

from flask import render_template

@app.route('/')
def root():

    labels, values = make_data_for_demograph()

    return render_template('index.html', labels=labels[:], values=values[:])

from .commons import Commons
import requests

@app.route('/apidemo')
def apidemo():

    sample_url= "{}/{}".format(Commons._OSRS_API, 
        "catalogue/detail.json?item=50")
    response = requests.get(sample_url).json()
    return jsonify(response)

import time

def current_milli_time():
    return round(time.time() * 1000)

from datetime import datetime

"""
    Need to Setup this User Agent for RuneWiki Real-time pricing apph
meseries?id=4151

ehrmagerd this data is good!:
https://prices.runescape.wiki/api/v1/osrs/timeseries?id=4151&timestep=5m
"""

session = requests.Session()
session.headers = {
    'User-Agent': 'APITesting/1.0',
    'From': 'pietari.poutiainen@gmail.com'  # This is another valid field
}

@app.route('/graphdemo')
def graphdemo():


    labels, values = make_data_for_demograph()
    return render_template("graphdemo.html", labels=labels[-20:], values=values[-20:])

def make_data_for_demograph() -> (list, list):

    sample_url = "{}/{}".format(Commons._OSRS_API, "graph/4151.json")
    response = requests.get(sample_url).json()

    data = response['daily']

    labels = []
    values = []


    for (l, v) in data.items():
        timestamp = int(l) / 1000.0
        label = datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d %H:%M:%s')
        labels.append(label)
        values.append(v)
    

    return labels, values