from getrecked import app
from flask import jsonify, render_template, request, send_from_directory
import time
from datetime import datetime
from dataclasses import dataclass
import requests
from typing import List
import os
import json

from .commons import Commons
from .db.database import Database
from .db.schema.item import Item
from .db.schema.volume import Volume
from .wiki_endpoint import WikiEndpoint

@dataclass
class Entry3Item:
    name: str
    examine: str
    id: int
    members: bool
    lowalch: int
    highalch: int
    limit: int
    value: int
    icon: str
    high_price: int
    low_price: int
    roi: float
    volume: int


@app.route('/journal')
def journal():

    labels, values = make_data_for_demograph()
    items: List[Item] = fetch_data_for_entry2table()
    
    entry3items = fetch_data_for_entry3_table(items)

    return render_template(
        'journal/index.html', 
        labels=labels[:], 
        values=values[:], 
        items=items, 
        entry3items=entry3items
    )

@app.route('/journal/graph_data', methods=["POST"])
def journal_graph_data():
    item_name = request.get_json()['item_name']
    item_id = int(request.get_json()['item_id'])
    return jsonify(make_data_for_graph(item_id))
    #return "{} with id {} is a nice item".format(item_name, item_id)

def make_data_for_graph(item_id: int):
    ret = "{}"
    graph_data = WikiEndpoint.fetch_timeseries_5m(int(item_id))

    data = graph_data['data']

    high_prices = []
    hp_timestamps = []

    for entry in data:
        if entry['avgHighPrice']:
            high_prices.append(entry['avgHighPrice'])
            _seconds = int(entry['timestamp'])
            lbl = datetime.fromtimestamp(_seconds).strftime('%Y/%m/%d %H:%M:%S')
            hp_timestamps.append(lbl)

    ret = {
        "price": high_prices,
        "timestamp": hp_timestamps
    }
    return ret

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

def fetch_data_for_entry2table() -> List[Item]:

    db = Database()
    cur = db.get_db().cursor()
    cur.execute("SELECT * FROM Item WHERE Item.name LIKE '%mole%'")
    items = cur.fetchall()
    items_dc = []
    for item in items:
        items_dc.append(Item(*item))
    return items_dc

def fetch_data_for_entry3_table(items: List[Item]) -> List[Entry3Item]:

    entry3_data: List[Entry3Item] = []
    for item in items:
        record = fetch_entry3item_data(item)
        entry3_data.append(record)

    return entry3_data

def fetch_entry3item_data(item: Item) -> Entry3Item:

    db = Database()
    cur = db.get_db().cursor()
    
    cur.execute("SELECT * FROM Volume WHERE Volume.item_id==?", (item.id, ))
    match = cur.fetchall()
    assert len(match) == 1, "There should be one volume per item"
    item_vol: Volume = Volume(*match[0])

    item_hl = WikiEndpoint.fetch_high_low_data(item.id)
    record = Entry3Item(
        name = item.name,
        examine = item.examine,
        id = item.id,
        members = item.members,
        lowalch = item.low_alch,
        highalch = item.high_alch,
        limit = item.ge_limit,
        value = item.value,
        icon = item.icon,
        high_price = item_hl['high'],
        low_price = item_hl['low'],
        roi = ((item_hl['high'] / item_hl['low']) - 1) * 100,
        volume = item_vol.volume
    )

    return record
