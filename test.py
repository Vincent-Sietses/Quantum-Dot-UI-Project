from bokeh.io import push_notebook, show, output_notebook, curdoc
from bokeh.palettes import brewer , inferno
from bokeh.models import ColumnDataSource, Select, ColorBar, BasicTicker, LinearColorMapper, Div, Slider, Spinner
from bokeh.layouts import row, gridplot, column
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import layout
from random import random
from time import time
import numpy as np

#TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

roots = [0 + 0j, 0 + 0j ]
def evaluate_polynomial(real, img):
    return np.product([z - real - img*1j for z in roots], axis = 0) 


p_real = figure(title="Real Part of Polynomial", tools=TOOLS)  

p_img = figure(title="Imaginary Part of Polynomial", tools=TOOLS)  
p_real.sizing_mode = 'scale_width'
p_img.sizing_mode = 'scale_width'
x , y  = np.linspace(-5, 5, 100) , np.linspace(-5, 5, 100)
xv, yv = np.meshgrid(x, y, sparse=True)
initial_image = evaluate_polynomial(xv, yv)
#H = np.outer(x,y)
start_time = time()


source_real = ColumnDataSource(dict(Hs=[]))
source_img = ColumnDataSource(dict(Hs=[]))

pallette = inferno(56)

color_mapper_real = LinearColorMapper(palette=pallette, low=np.min(np.real(initial_image)), high=np.max(np.real(initial_image)))
color_mapper_img = LinearColorMapper(palette=pallette, low=np.min(np.imag(initial_image)), high=np.max(np.imag(initial_image)))
p_real.image(image="Hs", x=-5, y=-5, dw=10  , dh=10, color_mapper=color_mapper_real,  source = source_real)
p_img.image(image="Hs", x=-5, y=-5, dw=10  , dh=10, color_mapper=color_mapper_img,  source = source_img)

color_bar_real = ColorBar(color_mapper=color_mapper_real,  ticker=BasicTicker(desired_num_ticks=len(pallette)+1),)
color_bar_img = ColorBar(color_mapper=color_mapper_img,  ticker=BasicTicker(desired_num_ticks=len(pallette)+1),)

def create_value():
    # for polynomial
    P = evaluate_polynomial(xv, yv)
    return P + P * 0.02 * (time() - start_time)* np.random.rand(* P.shape)
    
    # for outer prod graph
    #return np.outer(x,y) +  (time() - start_time)* np.random.rand(* H.shape)
      


def update():
    newH = create_value()
    new_data_real = dict(Hs=[np.real(newH)])
    new_data_img = dict(Hs=[np.imag(newH)])
    source_real.stream(new_data_real, rollover=0)
    source_img.stream(new_data_img, rollover=0)
    
    # attempt to update color bar bounds didnt go very well : 
    #
    # new_color_mapper = LinearColorMapper(palette="Spectral11", low=np.min(H), high=np.max(H))
    # if np.min(newH) < color_bar.color_mapper.low : 
    #     color_bar.color_mapper.low = np.min(H)
    #     p.right[0] = ColorBar(color_mapper=new_color_mapper)
    #     r.color_mapper = new_color_mapper
    # if np.max(newH) > color_bar.color_mapper.high : 
    #     color_bar.color_mapper.high = np.max(H)
    #     p.right[0] = ColorBar(color_mapper=new_color_mapper)
    #     r.color_mapper = new_color_mapper

slider_z1r = Slider(
    title="Real part of root 1",
    start=-5,
    end=5,
    step=0.1,
    value= 0 ,
)

def slider_z1r_callback(attr, old, new):
    global roots
    roots[0] = np.imag(roots[0]) * 1j + new 

slider_z1r.on_change("value", slider_z1r_callback)

slider_z1i = Slider(
    title="Imaginary part of root 1",
    start=-5,
    end=5,
    step=0.1,
    value= 0 ,
)

def slider_z1i_callback(attr, old, new):
    global roots
    roots[0] = np.real(roots[0])  + new * 1j

slider_z1i.on_change("value", slider_z1i_callback)


p_real.add_layout(color_bar_real, 'right')
p_img.add_layout(color_bar_img, 'right')
	 
lay_out = layout([[slider_z1r, slider_z1i],[p_real, p_img]])
curdoc().theme = "dark_minimal"
curdoc().title = "Instrument UI"
curdoc().add_root(lay_out)
curdoc().add_periodic_callback(update, 500)
 