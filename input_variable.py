# most imports are not required but for programming convenience I'll leave them in here

from bokeh.io import push_notebook, show, output_notebook, curdoc
from bokeh.palettes import brewer , inferno
from bokeh.models import Div, Button, ColumnDataSource, Select, ColorBar, BasicTicker, LinearColorMapper, Div, Slider, Spinner
from bokeh.layouts import row, gridplot, column
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import layout
from random import random
from time import time
from math import log10 , floor, ceil
import numpy as np

class InputVariable :
    """
    This class holds the UI as well as the value of a variable 
    Its purpose is to link the UI and the measurement 
    """
    def __init__(self,
                 set_variable ,
                 get_variable , 
                 variable_name: str = "generic variable",
                 unit : str = "", initial_value : float = 0,
                 initial_stepsize: float = None,
                 variable_resolution : float = 2e-5,
                 stepsize_lower_bound : float = 1e-6,
                 stepsize_upper_bound : float = 1,
                 ): 
        self.get_variable = get_variable
        self.set_variable = set_variable
        self.unit = unit
        self.value = self.get_variable()
        
        if initial_stepsize:
            self.stepsize = initial_stepsize
        else:
            self.stepsize = max(stepsize_lower_bound,  min(10 * variable_resolution, stepsize_upper_bound))
        
        self.variable_name = variable_name
        self.variable_resolution = variable_resolution
        self.stepsize_lower_bound = stepsize_lower_bound
        self.stepsize_upper_bound = stepsize_upper_bound
        
        
        self.ui_row = self.create_widget()
        
       

    def create_widget(self):
        self.value_div = Div(
              text=f"""
            <center><p> {self.variable_name} :  {self.value:E} {self.unit} </p></center>
                """,
                 style={'text-align': 'center',  'color': 'black'},
    width=150,
    height=80
        )
        
        self.step_div = Div(
              text=f"""
            <center><p> Stepsize :  {self.stepsize:E} {self.unit} </p></center>
                """,
                 style={'text-align': 'center',  'color': 'black'},
    width=150,
    height=80
        )
        
        self.plus_button = Button(
                                    label = "???",
                                    width=60,
                                    height=30
                                   )
        
        def plus_button_clicked():
            self.value = get_variable()
            self.value += self.stepsize 
            self.set_variable(self.value) 
            self.value_div.text = f"""
            <center><p> {self.variable_name} :  {self.value:E} {self.unit} </p></center>
                """
            
            
        self.plus_button.on_click(plus_button_clicked)
        
        
        self.minus_button = Button(
                                    label = "???",
                                    width=60,
                                    height=30
                                   )
        
        def minus_button_clicked():
            self.value = get_variable()
            self.value -= self.stepsize 
            self.set_variable(self.value)
            self.value_div.text = f"""
            <center><p> {self.variable_name} :  {self.value:E} {self.unit} </p></center>
                """
            
        
        self.minus_button.on_click(minus_button_clicked)
        
        
        self.plus_button_step = Button(
                                    label = "???",
                                    width=60,
                                    height=30
                                   )
        
        def plus_button_step_clicked():
            
                
            self.stepsize = min(self.stepsize_upper_bound, self.stepsize + self.variable_resolution)
                
            self.step_div.text = f"""
            <center><p> Stepsize :  {self.stepsize:E} {self.unit} </p></center>
                """
            
            
        self.plus_button_step.on_click(plus_button_step_clicked)
        
        
        self.minus_button_step = Button(
                                    label = "???",
                                    width=60,
                                    height=30
                                   )
        
        def minus_button_step_clicked():
           
            
            self.stepsize = max(self.stepsize_lower_bound, self.stepsize - self.variable_resolution)
                
                
            self.step_div.text = f"""
            <center><p> Stepsize :  {self.stepsize:E} {self.unit} </p></center>
                """
        
        self.minus_button_step.on_click(minus_button_step_clicked)
        
        
        
         
        
        return row( column(self.plus_button,self.minus_button), self.value_div, column( self.plus_button_step, self.minus_button_step), self.step_div,)