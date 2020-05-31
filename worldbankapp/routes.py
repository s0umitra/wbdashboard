from worldbankapp import app
import json, plotly
from flask import render_template
from wrangling_scripts.wrangle_data import return_figures


@app.route('/')
@app.route('/index')
def index():
    figures = return_figures()

    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)
