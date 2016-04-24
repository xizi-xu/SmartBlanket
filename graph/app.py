from flask import Flask, jsonify, json, render_template, request, url_for
# abort, flash, redirect
import datetime
from dateutil.relativedelta import relativedelta
import random
from collections import defaultdict
import pygal
from pygal.style import CleanStyle
import pymongo

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
    ten_am = datetime.time(hour=1)
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

data_set = []
for i in range(0, 5):
    data_set.append(generate_mock_data())

@app.route('/get_data')
def get_data():
    return jsonify(data_set[0])

@app.route('/preferences')
def get_preferences():
    now = datetime.datetime.now()
    pref = []
    for i in range(20):
        pref += [73 + i]*5

    return jsonify({"preferences": [80, 70, 104.9, 91.12]})


@app.route('/graph')
def draw_line_graph(interval = 'fifteen_minute_interval'):
    # interval = 'one_minute_interval'
    # get data and time duration
    current_date = data_set[0]['date']
    times = [str(i[0]) for i in data_set[0][interval]]
    # create a bar chart
    title = 'Temperature for %s' % current_date.strftime("%Y-%m-%d")
    bar_chart = pygal.Line(width=1200, height=600,
                          explicit_size=True, title=title, x_label_rotation=40, style=CleanStyle)
    # add time label
    bar_chart.x_labels = times
    # add line plots
    sensorNum = 1
    for sensor in data_set:
        temp_reading = sensor[interval]
        imp_temps = [float(i[1]) for i in temp_reading]
        temp_label = 'Sensor ' + str(sensorNum)
        bar_chart.add(temp_label, imp_temps)
        sensorNum += 1

    # html = """
    #     <html>
    #          <head>
    #               <title>%s</title>
    #          </head>
    #           <body>
    #              %s
    #          </body>
    #     </html>
    #     """ % (title, bar_chart.render())
    html = """
        %s
        """ % bar_chart.render()
    return html.decode("utf8")

@app.route('/')
def main():
    return render_template('index.html', graph15 = draw_line_graph(), graph1 = draw_line_graph('one_minute_interval'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
