from bokeh.io import push_notebook, show, output_notebook, curdoc
from bokeh.palettes import brewer , inferno, viridis, cividis , plasma
from bokeh.models import ColumnDataSource, Select, ColorBar, BasicTicker, LinearColorMapper, Div, Slider, Spinner, Dropdown
from bokeh.layouts import row, gridplot, column
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import layout
from random import random
from time import time
import numpy as np


from input_variable import InputVariable
from draw_plot import generate_plot


def evaluate_polynomial(real, img, measurement_variables):
    roots = [
        measurement_variables[0].value + measurement_variables[1].value * 1j,
        measurement_variables[2].value + measurement_variables[3].value * 1j,
    ]
    return np.product([z - real - img*1j for z in roots], axis = 0)

def run_demo(
                plot_title = "Demo plot", 
                CALLBACK_TIME_MS = 500,
                plot_x=-1,  # plot axis parameters
                plot_y=-1,  # plot axis parameters
                plot_dw=2, # plot axis parameters
                plot_dh=2, # plot axis parameters
            ):
    
    
    #TOOLS define the default Bokeh graph tools 
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
    
    plot = figure(title= plot_title, tools=TOOLS,  plot_width=400, plot_height=400)  
    #plot.sizing_mode = 'scale_width'
    
    
    # import variables from variables file
    from demo_variables import generate_variables
    measurement_variables = generate_variables()



    x , y  = np.linspace(plot_x, plot_x + plot_dw, 100) , np.linspace(plot_y, plot_y + plot_dh, 100)
    xv, yv = np.meshgrid(x, y, sparse=True)
    initial_image = evaluate_polynomial(xv, yv, measurement_variables)
    
    # record time to increase noise overtime
    start_time = time()


    source = ColumnDataSource(dict(Hs=[]))
     
    color_palette = inferno(80) # max : 256
 
    color_mapper = LinearColorMapper(palette=color_palette, 
                                    low=np.min(np.abs(initial_image)), 
                                    high=np.max(np.abs(initial_image)))
    

    img = plot.image(image='Hs', 
                 x=plot_x, 
                 y=plot_y, 
                 dw=plot_dw, 
                 dh=plot_dh, 
                 color_mapper=color_mapper,  
                 source = source)
    
    color_bar = ColorBar(color_mapper=color_mapper,  ticker=BasicTicker(desired_num_ticks=len(color_palette)+1),)
    
    plot.add_layout(color_bar, 'right')


    def create_value():
        P = evaluate_polynomial(xv, yv, measurement_variables)
        return np.abs(P + P * 0.02 * np.sqrt(time() - start_time)* np.random.rand(* P.shape) ) 
        

    def update(new_color_palette = None):
        
        newimage= create_value()
        new_data = dict(Hs=[newimage])
        source.stream(new_data , rollover=1)
        
        if new_color_palette:
            
            img.glyph.color_mapper = LinearColorMapper(palette=new_color_palette, 
                                    low=np.min(newimage), 
                                    high=np.max(newimage))
            color_bar.color_mapper.update(palette=new_color_palette, 
                                    low=np.min(newimage), 
                                    high=np.max(newimage))
            
            
         
         
    
    color_dropdown = Dropdown(label='Select plot color', menu=['brewer', 'plasma' , 'inferno', 'viridis', 'cividis' ])


    def dropdown_handler(event):
        #handle dropdown input
        color_palette = None
        if event.item == 'brewer':
            color_palette = brewer['RdYlBu'][10]
        elif event.item == "inferno":
            color_palette = inferno(80)
        elif event.item == "viridis":
            color_palette = viridis(80)
        elif event.item == 'plasma':
            color_palette = plasma(80)
        else:
            color_palette = cividis(80)
        
        update(new_color_palette=color_palette)
        
    color_dropdown.on_click(dropdown_handler)
    
    lay_out = layout(row(  
                      column(*[v.ui_row for v in measurement_variables]),
                      column(color_dropdown,plot, 
                             )
    ))
    
    
    curdoc().theme = "dark_minimal"
    curdoc().title = "Instrument UI"
    curdoc().add_root(lay_out)
    curdoc().add_periodic_callback(update, CALLBACK_TIME_MS)
    