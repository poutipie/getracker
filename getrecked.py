from pdb import Pdb
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


@app.route('/item_data', methods=["POST"])
def item_data() -> List[Item]:

    db = Database()
    cur = db.get_db().cursor()
    cur.execute("SELECT * FROM Item LIMIT 20;")
    items_raw: tuple = cur.fetchall()
    items: list = [Item(*item)._asdict() for item in items_raw]

    return jsonify(items)


@app.route('/chart_5m', methods=["POST"])
def chart_5m():

    item_id = int(request.get_json()['item_id'])
    return jsonify(make_data_for_graph(item_id))

def make_data_for_graph(item_id: int):

    item: Item = _fetch_item_from_db(item_id)

    graph_data = WikiEndpoint.fetch_timeseries_5m(int(item_id))
    data = graph_data['data']

    high_prices = []
    high_timestamps = []

    for entry in data:
        if entry['avgHighPrice']:
            high_prices.append(entry['avgHighPrice'])
            _seconds = int(entry['timestamp'])
            lbl = datetime.fromtimestamp(_seconds).strftime('%Y/%m/%d %H:%M:%S')
            high_timestamps.append(lbl)


    return {
        "item_name": item.name,
        "high_timestamps": high_timestamps,
        "high_prices": high_prices
    }

def _fetch_item_from_db(item_id: int) -> Item:

    db = Database()
    cur = db.get_db().cursor()

    #import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

    cur.execute("SELECT * FROM Item Where Item.id == ?", (str(item_id),))
    item_raw: tuple = cur.fetchall()[0]
    return Item(*item_raw)
