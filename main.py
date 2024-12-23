import base64
from flask import Flask, render_template
from io import BytesIO

import json
from matplotlib.figure import Figure
app = Flask(__name__)


def read_data():
    f = open('data.json')
    data = json.load(f)
    return data
   
def create_graph(time_used, time_budget):
    fig = Figure(figsize=(5,5))
    ax = fig.subplots()
    data = [time_used, max(time_budget-time_used,0)]
    colors = ['blue', 'grey']
    text_color = 'white'
    
    # generate graph and text
    ax.pie(data, colors=colors, wedgeprops={'width': 0.4}, startangle=90, counterclock=False, radius=1)

    # time limit exceed
    if time_used > time_budget:
        overtime = time_used - time_budget
        ax.pie([overtime, time_budget], colors=['red','black'], wedgeprops={'width': 0.4}, startangle=90, counterclock=False, radius=1.4)
        text_color = 'red'
    ax.text(0, 0, '{}/{}'.format(time_used, time_budget), horizontalalignment='center', verticalalignment='center', fontsize=60, color=text_color)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png", transparent=True)
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def generate_graphs():
    data = read_data()
    titles = []
    graphs = []
    for i in data["budgets"]:
        title = i["title"]
        time_budget = i["budget"]
        time_used = i["used"]
        refresh_rate = i["refresh"]
        graphs.append(create_graph(time_used, time_budget))
        titles.append(title)
    return titles, graphs


@app.route("/")
def hello_world():
    titles, graphs = generate_graphs()
    return render_template('index.html',titles=titles, graphs=graphs, len=len(graphs))

