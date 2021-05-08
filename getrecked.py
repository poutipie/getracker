from getrecked import app
from flask import jsonify, render_template
import time
from datetime import datetime
from dataclasses import dataclass
import requests
from typing import List

from .commons import Commons
from .db.database import Database
from .db.schema.item import Item
from .wiki_endpoint import WikiEndpoint

VOLUMES = None

@dataclass
class ItemOverview:
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


@app.route('/')
def root():
    
    VOLUMES = WikiEndpoint.fetch_volumes()

    labels, values = make_data_for_demograph()

    items: List[Item] = fetch_data_for_entry2table()
    entry3items = fetch_data_for_entry3_table(items, VOLUMES)
    return render_template(
        'index.html', 
        labels=labels[:], 
        values=values[:], 
        items=items[:15], 
        entry3items=entry3items
    )

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
    
    cur.execute("SELECT * FROM Item LIMIT 5")
    items = cur.fetchall()
    items_dc = []
    for item in items:
        items_dc.append(Item(*item))
    return items_dc

def fetch_data_for_entry3_table(items: List[Item], volumes):

    entry3_data = []
    for item in items:
        record = fetch_record_data_for_item_mapping(item, volumes)
        entry3_data.append(record)

    return entry3_data

def fetch_record_data_for_item_mapping(item: Item, volumes):

    item_hl = WikiEndpoint.fetch_high_low_data(item.id)
    record = ItemOverview(
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
        volume = volumes[str(item.id)]
    )

    return record
