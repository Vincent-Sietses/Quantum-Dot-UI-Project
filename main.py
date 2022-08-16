# imports 
from bokeh.io import push_notebook, show, output_notebook, curdoc
from bokeh.palettes import brewer , inferno
from bokeh.models import ColumnDataSource, Select, ColorBar, BasicTicker, LinearColorMapper, Div, Slider, Spinner
from bokeh.layouts import row, gridplot, column
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import layout
from random import random
from time import time
import numpy as np

# set mode here
# set to 0 for the demo (plots a complex quadratic with roots managed by a slider)
# set to 1 functional QDUI ( work in progress)
UI_MODE = 0 


# Refresh rate
CALLBACK_TIME_MS = 750

if UI_MODE == 0 : 
    # import demo.py file from repo
    from demo import run_demo
    run_demo(CALLBACK_TIME_MS = CALLBACK_TIME_MS)