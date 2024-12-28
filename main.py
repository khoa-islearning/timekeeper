import base64
from flask import Flask, render_template
from io import BytesIO

import json

from pygal import style
# from matplotlib.figure import Figure
app = Flask(__name__)
import pygal
from pygal.style import Style


def read_data():
    f = open('data.json')
    data = json.load(f)
    return data
   
#def create_graph_matplot (time_used, time_budget):
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

def create_graph_pygal(time_used, time_budget, title):
    time_remained = max(time_budget-time_used, 0)
    custom_style = Style(
            background='transparent',
            plot_background='transparent',
            foreground_strong='white' if time_remained > 0 else '#FF3D00', # the box
            foreground_subtle='#FF6F00', # the label
            opacity='.4',
            opacity_hover='.1',
            transition='400ms ease-in',
            colors=('#00BFAE', '#BDC3C7') if time_remained > 0 else ('#FF3D00', '#BDC3C7'),
            font_family='googlefont:Ubuntu',
            title_font_family='googlefont:Montserrat',
            title_font_size=60
            )
    
    pie_chart = pygal.Pie(style = custom_style, half_pie=True, inner_radius=.4)
    pie_chart.show_legend = False
    pie_chart.add('time_used', time_used)
    pie_chart.add('time_budget', time_remained)
    pie_chart.title = title.upper()
    svg = pie_chart.render_data_uri()

    return svg

def generate_graphs():
    data = read_data()
    titles = []
    graphs = []
    for i in data["budgets"]:
        title = i["title"]
        time_budget = i["budget"]
        time_used = i["used"]
        refresh_rate = i["refresh"]
        graphs.append(create_graph_pygal(time_used, time_budget, title))
        titles.append(title)
    return titles, graphs


@app.route("/")
def hello_world():
    titles, graphs = generate_graphs()
    return render_template('index.html',titles=titles, graphs=graphs, len=len(graphs))

