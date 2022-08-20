from bokeh.io import push_notebook, show, output_notebook, curdoc
from bokeh.palettes import brewer , inferno, viridis, cividis 
from bokeh.models import ColumnDataSource, Select, ColorBar, BasicTicker, LinearColorMapper, Div, Slider, Spinner, Dropdown
from bokeh.layouts import row, gridplot, column
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import layout
from random import random
from time import time
import numpy as np


from input_variable import InputVariable

def run_demo(plot_title = "Demo plot", CALLBACK_TIME_MS = 500,):
    #TOOLS define the default Bokeh graph tools 
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
    
    # import variables from variables file
    from demo_variables import generate_variables
    measurement_variables = generate_variables()


    #roots = [0 + 0j, 0 + 0j, ]
    
    
    
    def evaluate_polynomial(real, img):
        roots = [
            measurement_variables[0].value + measurement_variables[1].value * 1j,
            measurement_variables[2].value + measurement_variables[3].value * 1j,
        ]
        return np.product([z - real - img*1j for z in roots], axis = 0) 


    p_real = figure(title="Modulus of Polynomial ", tools=TOOLS)  

    
    p_real.sizing_mode = 'scale_width'
     
    x , y  = np.linspace(-5, 5, 100) , np.linspace(-5, 5, 100)
    xv, yv = np.meshgrid(x, y, sparse=True)
    initial_image = evaluate_polynomial(xv, yv)
    #H = np.outer(x,y)
    start_time = time()


    image_source = ColumnDataSource(dict(images=[]))
    #source_img = ColumnDataSource(dict(Hs=[]))

    pallette = inferno(80) # max : 256

    color_mapper_real = LinearColorMapper(palette=pallette, low=np.min(np.abs(initial_image)), high=np.max(np.abs(initial_image)))
    #color_mapper_img = LinearColorMapper(palette=pallette, low=np.min(np.imag(initial_image)), high=np.max(np.imag(initial_image)))
    p_real.image(image="images", x=-5, y=-5, dw=10  , dh=10, color_mapper=color_mapper_real,  source = source_real)
    #p_img.image(image="Hs", x=-5, y=-5, dw=10  , dh=10, color_mapper=color_mapper_img,  source = source_img)

    color_bar_real = ColorBar(color_mapper=color_mapper_real,  ticker=BasicTicker(desired_num_ticks=len(pallette)+1),)
    #color_bar_img = ColorBar(color_mapper=color_mapper_img,  ticker=BasicTicker(desired_num_ticks=len(pallette)+1),)

    def create_value():
        P = evaluate_polynomial(xv, yv)
        return P + P * 0.02 * np.sqrt(time() - start_time)* np.random.rand(* P.shape)
        

    def update():
        newimage= create_value()
        new_data_real = dict(images=[np.abs(newimage)])
        #new_data_img = dict(Hs=[np.imag(newH)])
        source_real.stream(new_data_real, rollover=0)
        #source_img.stream(new_data_img, rollover=0)
        
    
   
    p_real.add_layout(color_bar_real, 'right')
    #p_img.add_layout(color_bar_img, 'right')
    
    color_dropdown = Dropdown(label='Select plot color', menu=['brewer' , 'inferno', 'viridis', 'cividis' ])


    def handler(event):
        #handle dropdown input
        print(event.item)


    color_dropdown.on_click(handler)
    
    lay_out = layout(row(  
                      column(*[v.ui_row for v in measurement_variables]),
                      column(color_dropdown,p_real,# p_img
                             )
    ))
    
    
    curdoc().theme = "dark_minimal"
    curdoc().title = "Instrument UI"
    curdoc().add_root(lay_out)
    curdoc().add_periodic_callback(update, CALLBACK_TIME_MS)
    