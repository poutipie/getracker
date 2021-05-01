from getrecked import app
from flask import jsonify, render_template
from .commons import Commons
import time
from datetime import datetime

@app.route('/')
def root():

    labels, values = make_data_for_demograph()


    items = fetch_data_for_entry2table()
    return render_template('index.html', labels=labels[:], values=values[:], items=items[:5])

def make_data_for_demograph() -> (list, list):

    sample_url = "{}/{}".format(Commons._OSRS_API, "graph/4151.json")
    response = Commons.session().get(sample_url).json()
    data = response['daily']

    labels = []
    values = []
    for (l, v) in data.items():
        timestamp = int(l) / 1000.0
        label = datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d %H:%M:%s')
        labels.append(label)
        values.append(v)
    
    return labels, values

def fetch_data_for_entry2table():

    url: str = "{}/{}".format(Commons._OSRS_WIKI_API, "mapping")
    response = Commons.session().get(url).json()

    """
    {
        'examine': 'A fabulously ancient gnarled staff as used by the druids of old.', 
        'id': 23342, 
        'members': True, 
        'lowalch': 80000, 
        'limit': 8, 
        'value': 200000, 
        'highalch': 120000, 
        'icon': '3rd age druidic staff.png', 
        'name': '3rd age druidic staff'
    }
    """
    return response