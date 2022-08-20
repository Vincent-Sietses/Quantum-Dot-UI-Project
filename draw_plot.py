from bokeh.io import push_notebook, show, output_notebook, curdoc
from bokeh.palettes import brewer , inferno, viridis, cividis 
from bokeh.models import ColumnDataSource, Select, ColorBar, BasicTicker, LinearColorMapper, Div, Slider, Spinner, Dropdown
from bokeh.layouts import row, gridplot, column
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import layout
from random import random
from time import time
import numpy as np



def generate_plot(plot_title, 
                  palette, 
                  initial_image, 
                  image_source,
                  x=-5,  # plot axis parameters
                  y=-5,  # plot axis parameters
                  dw=10, # plot axis parameters
                  dh=10, # plot axis parameters
                  ):
    
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
    
    plot = figure(title="Modulus of Polynomial ", tools=TOOLS)  
    
    plot.sizing_mode = 'scale_width'
    
    color_mapper = LinearColorMapper(palette=pallette, low=np.min(np.abs(initial_image)), high=np.max(np.abs(initial_image)))
    
    
    p_real.image(image="images", 
                 x=x, 
                 y=y, 
                 dw=dw  , 
                 dh=dh, 
                 color_mapper=color_mapper,  
                 source = image_source)
    