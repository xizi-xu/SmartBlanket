from flask import Flask, jsonify
import datetime
from dateutil.relativedelta import relativedelta
import random
from collections import defaultdict


import pygal
import json

WELL_FORMED_DATA = True

app = Flask(__name__)

def date_range(start_date, end_date, increment, period):
    result = []
    nxt = start_date
    delta = relativedelta(**{period:increment})
    while nxt <= end_date:
        result.append(nxt)
        nxt += delta
    return result

def generate_mock_data():
    today = datetime.datetime.now().date()
    ten_am = datetime.time(hour=10)
    eight_pm = datetime.time(hour=20)

    end_time = datetime.datetime.combine(today, ten_am)
    start_time = datetime.datetime.combine(today - datetime.timedelta(1), eight_pm)

    fifteen_mins_data = defaultdict(lambda: None)
    fifteen_minute_intervals = date_range(start_time, end_time, 15, 'minutes')
    for i in fifteen_minute_intervals:
        if WELL_FORMED_DATA:
            fifteen_mins_data[i] = random.randint(70, 100)
        elif random.randint(0, 1):
            fifteen_mins_data[i] = random.randint(70, 100)

    one_min_data = defaultdict(lambda: None)
    minute_intervals = date_range(start_time, end_time, 1, 'minutes')
    for i in minute_intervals:
        if WELL_FORMED_DATA:
            one_min_data[i] = random.randint(70, 100)
        elif random.randint(0, 1):
            one_min_data[i] = random.randint(70, 100)

    ret_val = {
        "date": datetime.datetime.now(),
        "fifteen_minute_interval": [(t.strftime("%H:%M"), fifteen_mins_data[t]) for t in fifteen_minute_intervals],
        "one_minute_interval": [(t.strftime("%H:%M"), one_min_data[t]) for t in minute_intervals]
    }

    # return jsonify(ret_val)
    return ret_val

@app.route('/get_data')
def get_data():
    return jsonify(generate_mock_data())

@app.route('/graph')
def draw_line_graph():
    parsed = generate_mock_data()
    current_date = parsed['date']
    fifteen_min = parsed['fifteen_minute_interval']
    imp_temps = [float(i[1]) for i in fifteen_min]
    times = [str(i[0]) for i in fifteen_min]
    # create a bar chart
    title = 'Temps for %s' % current_date.strftime("%Y-%m-%d %H:%M:%S")
    bar_chart = pygal.Line(width=1200, height=600,
                          explicit_size=True, title=title, x_label_rotation=40)
    bar_chart.x_labels = times
    bar_chart.add('Sensor1', imp_temps)

    fifteen_min2 = generate_mock_data()['fifteen_minute_interval']
    fifteen_min3 = generate_mock_data()['fifteen_minute_interval']
    fifteen_min4 = generate_mock_data()['fifteen_minute_interval']
    fifteen_min5 = generate_mock_data()['fifteen_minute_interval']
    imp_temps2 = [float(i[1]) for i in fifteen_min2]
    imp_temps3 = [float(i[1]) for i in fifteen_min3]
    imp_temps4 = [float(i[1]) for i in fifteen_min4]
    imp_temps5 = [float(i[1]) for i in fifteen_min5]

    bar_chart.add('Sensor2', imp_temps2)
    bar_chart.add('Sensor3', imp_temps3)
    bar_chart.add('Sensor4', imp_temps4)

    html = """
        <html>
             <head>
                  <title>%s</title>
             </head>
              <body>
                 %s
             </body>
        </html>
        """ % (title, bar_chart.render())
    return html

if __name__ == '__main__':
    app.run(debug=True)
