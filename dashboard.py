import sqlite3
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1('Bee Monitor Dashboard'),
    dcc.Interval(id='graph-update', interval=1000),
    dcc.Graph(id='time'),
    dcc.Graph(id='size'),
    dcc.Graph(id='speed')
])

@app.callback(Output('time', 'figure'), events=[Event('graph-update', 'interval')])
def updateTime():
    conn = sqlite3.connect('bees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT t.time FROM bees t ORDER BY t.time ASC;')
    data = cursor.fetchall()
    data = [datetime.strptime(d[0], "%Y-%m-%d %H:%M:%S") for d in data]
    return {'data': [{'x': data, 'type': 'histogram', 'name': 'Time'}],
            'layout': {'title': 'Traffic Volume'}}

@app.callback(Output('size', 'figure'), events=[Event('graph-update', 'interval')])
def updateSize():
    conn = sqlite3.connect('bees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT t.size FROM bees t;')
    data = cursor.fetchall()
    data = [int(d[0]) for d in data]
    return {'data': [{'x': data, 'type': 'histogram', 'name': 'Size'}],
            'layout': {'title': 'Size'}}

@app.callback(Output('speed', 'figure'), events=[Event('graph-update', 'interval')])
def updateSize():
    conn = sqlite3.connect('bees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT t.speed FROM bees t;')
    data = cursor.fetchall()
    data = [abs(int(d[0])) for d in data]
    return {'data': [{'x': data, 'type': 'histogram', 'name': 'Speed'}],
            'layout': {'title': 'Speed'}}


if __name__ == '__main__':
    app.run_server(debug=True)
