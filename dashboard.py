import sqlite3
import sys
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, Event


def updateTime():
    conn = sqlite3.connect('bees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT t.time FROM bees t ORDER BY t.time ASC;')
    data = cursor.fetchall()
    data = [datetime.strptime(d[0], "%Y-%m-%d %H:%M:%S") for d in data]
    return {'data': [{'x': data, 'type': 'histogram', 'name': 'Time'}],
            'layout': {'title': 'Traffic Volume'}}


def updateSize():
    conn = sqlite3.connect('bees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT t.size FROM bees t;')
    data = cursor.fetchall()
    data = [int(d[0]) for d in data]
    return {'data': [{'x': data, 'type': 'histogram', 'name': 'Size'}],
            'layout': {'title': 'Size'}}


def updateSpeed():
    conn = sqlite3.connect('bees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT t.speed FROM bees t;')
    data = cursor.fetchall()
    data = [abs(int(d[0])) for d in data]
    return {'data': [{'x': data, 'type': 'histogram', 'name': 'Speed'}],
            'layout': {'title': 'Speed'}}


def updateTable():
    conn = sqlite3.connect('bees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT t.size, t.speed, t.time FROM bees t ORDER BY t.time DESC;')
    data = cursor.fetchall()
    return [{k:v for v,k in zip(r, ['size', 'speed', 'time'])} for r in data]


app = dash.Dash()
app.layout = html.Div(children=[
    html.H1('Bee Monitor Dashboard'),
    dcc.Interval(id='graph-update', interval=1000),
    dcc.Graph(id='time', figure=updateTime()),
    dcc.Graph(id='size', figure=updateSize()),
    dcc.Graph(id='speed', figure=updateSpeed()),
    dash_table.DataTable(
        id='table',
        columns=[{'id': x, 'name': x} for x in ['size', 'speed', 'time']],
        data=updateTable(),
        sorting=True,
        sorting_settings=[{'column_id':'time', 'direction':'desc'}],
        filtering=True
    )
])

app.callback(Output('time', 'figure'), events=[Event('graph-update', 'interval')])(updateTime)

app.callback(Output('size', 'figure'), events=[Event('graph-update', 'interval')])(updateSize)

app.callback(Output('speed', 'figure'), events=[Event('graph-update', 'interval')])(updateSpeed)

app.callback(Output('table', 'data'), events=[Event('graph-update', 'interval')])(updateTable)


if __name__ == '__main__':
    debug = len(sys.argv) > 1 and sys.argv[1] == '--debug'
        
    app.run_server(debug=debug)
