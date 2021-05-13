from pdb import Pdb
import sqlite3
import time
from datetime import datetime
from dataclasses import dataclass
from typing import List
import pandas

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

    filter: str = request.get_json()['filter']

    db: sqlite3.Connection = Database.connect()
    cur = db.cursor()
    if filter == '':
        query = "SELECT * FROM Item LIMIT 20;"
    else:
        query = "SELECT * FROM Item WHERE Item.name LIKE '%{}%' LIMIT 20;".format(filter)

    cur.execute(query)
    items_raw: tuple = cur.fetchall()
    Database.disconnect(db)
    items: list = [Item(*item)._asdict() for item in items_raw]

    return jsonify(items)


@app.route('/chart_5m', methods=["POST"])
def chart_5m():

    item_id = int(request.get_json()['item_id'])
    item: Item = _fetch_item_from_db(item_id)

    api_data = WikiEndpoint.fetch_timeseries_5m(item.id)
    graph_data = _format_graph_data(item, api_data)

    return jsonify(graph_data)

def _format_graph_data(item, api_data: list) -> list:
    
    data = api_data['data']

    df = pandas.DataFrame(data)
    df = df.set_index('timestamp')
    df_interp = df.interpolate().dropna()

    timestamps = []
    high_prices = []
    low_prices = []
    for row in df_interp.iterrows():
        entry = row[1]
        lbl = datetime.fromtimestamp(entry.name).strftime('%Y/%m/%d %H:%M:%S')
        timestamps.append(lbl)
        high_prices.append(entry['avgHighPrice'])
        low_prices.append(entry['avgLowPrice'])
    
    return {
        "item_name": item.name,
        "timestamps": timestamps,
        "high_prices": high_prices,
        "low_prices": low_prices
    }

def _fetch_item_from_db(item_id: int) -> Item:

    db: sqlite3.Connection = Database.connect()
    cur = db.cursor()
    cur.execute("SELECT * FROM Item Where Item.id == ?", (str(item_id),))
    item_raw: tuple = cur.fetchall()[0]
    Database.disconnect(db)
    return Item(*item_raw)
