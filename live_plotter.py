from bokeh.io import push_notebook, show, output_notebook, curdoc
from bokeh.palettes import brewer , inferno, viridis, cividis , plasma
from bokeh.models import ColumnDataSource, Select, ColorBar, BasicTicker, LinearColorMapper, Div, Slider, Spinner, Dropdown
from bokeh.layouts import row, gridplot, column
from bokeh.plotting import figure, show, output_file, output_notebook
from bokeh.layouts import layout

from random import random
from time import time

from bokeh.core.validation import silence 
from bokeh.core.validation.warnings import EMPTY_LAYOUT, MISSING_RENDERERS

import numpy as np

from input_variable import InputVariable

class LivePlotter:
    
    def __init__(self, plot_title = "Set Plot Title in LivePlotter(\"title\")"):
        TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
        self.plot = figure(title= plot_title, tools=TOOLS,  plot_width=500, plot_height=500)  
       
        # initialize settable attributes
        self.callback_time = None
        self.measurement_function = None
        self.plot_x = None
        
        # List to store InputVariable objects , which contain the widgets and setters / getters 
        self.variable_list = []
        
        #output_notebook()

        
    def set_callback_time(self, val):
        """ Takes an integer as the callbacktime (in milliseconds)"""
        self.callback_time = val
    
    def set_x_label(self, label : str):
        """ Takes a string as the new x axis label """
        self.plot.xaxis.axis_label = label
        
    def set_y_label(self, label : str):
        """ Takes a string as the new y axis label """
        self.plot.yaxis.axis_label = label
        
    def add_variable_widget(self,set_variable , get_variable ,  **kwargs):
        """ Adds a variable and the corresponding widgets
            Input : setter function , getter function
            
            optional variable keyword arguments : 
            
            variable_name , 
            unit , 
            initial_value ,
            initial_stepsize , #  defaults to 10*resolution
            variable_resolution  ,
            stepsize_lower_bound ,
            stepsize_upper_bound ,
            ui_precision ,    
        """
        self.variable_list.append(
            InputVariable(
                set_variable=set_variable,
                get_variable=get_variable,
                **kwargs, # contains all stepsize, resolution details
                )
            )
    
    def set_measurement_function(self,func):
        self.measurement_function = func
        
        
    def set_plot_dimensions(self, minx , miny, maxx, maxy):
        """ Set the plot dimensions using the minimum and maximum x and y values """
        self.plot_x = minx
        self.plot_y = miny 
        self.plot_dw = maxx - minx
        self.plot_dh = maxy - miny
        
    def show(self):
        """ Display the interactive graph"""
        show(self.bkapp)
        
    def bkapp(self, doc):
        """ Bokeh document app""" 
        
        allow_websocket_origin=["*"]
        
        if not self.measurement_function:
            raise ValueError("No measurement function has been defined. Define one by calling set_measurement_function(self,func) ")
        
        if not self.callback_time:
            raise ValueError("No callback time has been defined. Define one by calling set_callback_time(self, val) ")

        if not self.plot_x:
            raise ValueError("No plot dimensions has been defined. Define one by calling set_plot_dimensions(self, minx , miny, maxx, maxy) ")

        source = ColumnDataSource(dict(images=[]))
        color_palette = inferno(80) # max : 256
        
        self.initial_image = self.measurement_function()

        color_mapper = LinearColorMapper(palette=color_palette, 
                                        low=np.min(np.abs(self.initial_image)), 
                                        high=np.max(np.abs(self.initial_image)))
        

        img = self.plot.image(image='images', 
                    x=self.plot_x, 
                    y=self.plot_y, 
                    dw=self.plot_dw, 
                    dh=self.plot_dh, 
                    color_mapper=color_mapper,  
                    source = source)
        
        color_bar = ColorBar(color_mapper=color_mapper,  ticker=BasicTicker(desired_num_ticks=len(color_palette)+1),)
        
        color_bar_plot = figure(height=300, width=100, toolbar_location=None, min_border=0, outline_line_color=None)
        color_bar_plot.add_layout(color_bar, 'right')

        def update(new_color_palette = None):
            """ 
            Update function called every callbacktime
            Calls the measurement function
            Also handles changing the color of the image ( This is necessary because the colormap needs the max and min of the image )
            """
            newimage= self.measurement_function()
            new_data = dict(images=[newimage])
            source.stream(new_data , rollover=1)
            
            if new_color_palette:
                
                img.glyph.color_mapper = LinearColorMapper(palette=new_color_palette, 
                                        low=np.min(newimage), 
                                        high=np.max(newimage))
                
                color_bar = ColorBar(color_mapper=img.glyph.color_mapper,  ticker=BasicTicker(desired_num_ticks=len(color_palette)+1),)
        
                lay_out.children.pop()
                color_bar_plot = figure(height=300, width=100, toolbar_location=None, min_border=0, outline_line_color=None)
                color_bar_plot.add_layout(color_bar, 'right')
                lay_out.children.append(color_bar_plot)
            
    
        color_dropdown = Dropdown(label='Select plot color', menu=['brewer (red/blue)', 'brewer (Purple/Orange)', 'plasma' , 'inferno', 'viridis', 'cividis' ])


        def dropdown_handler(event):
            """ Handles a change in the color dropdown menu """
             
            color_palette = None
            if event.item == 'brewer (Red/Blue)':
                color_palette = brewer['RdYlBu'][10]
            elif event.item == 'brewer (Purple/Orange)':
                color_palette = brewer['PuOr'][10]
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
        
        # put the widgets in a column 
        # # need to put the color_bar plot outside of the row, because otherwise the code updating it fails
        lay_out = layout( 
        row(column(*[v.ui_row for v in self.variable_list]), column(color_dropdown,self.plot,)) , color_bar_plot, 
        )
        
        
        ## these lines make sure Bokeh's warnings about the color bar plot are not shown 
        silence(EMPTY_LAYOUT, True)
        silence(MISSING_RENDERERS, True)
        
        doc.theme = "dark_minimal"
        doc.title = "Instrument UI"
        doc.add_root(lay_out)
        doc.add_periodic_callback(update, self.callback_time)
        
        