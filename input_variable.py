# most imports are not required but for programming convenience I'll leave them in here

from bokeh.io import push_notebook, show, output_notebook, curdoc
from bokeh.palettes import brewer , inferno
from bokeh.models import Div, Button, ColumnDataSource, Select, ColorBar, BasicTicker, LinearColorMapper, Div, Slider, Spinner
from bokeh.layouts import row, gridplot, column
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import layout
from random import random
from time import time
from math import log10 , floor
import numpy as np

class InputVariable :
    """
    This class holds the UI as well as the value of a variable 
    Its purpose is to link the UI and the measurement 
    """
    def __init__(self, variable_name: str = "generic variable", unit : str = "", initial_value : float = 0, stepsize: float = 0.1): 
        self.unit = unit
        self.value = initial_value
        self.stepsize = stepsize
        self.variable_name = variable_name
        self.ui_row = self.create_widget()
       
        

    def create_widget(self):
        self.value_div = Div(
              text=f"""
            <center><p> {self.variable_name} :  {self.value:.8E} {self.unit} </p></center>
                """,
                 style={'text-align': 'center',  'color': 'black'},
    width=600,
    height=80
        )
        
        self.step_div = Div(
              text=f"""
            <center><p> Stepsize :  {self.stepsize:.1E} {self.unit} </p></center>
                """,
                 style={'text-align': 'center',  'color': 'black'},
    width=600,
    height=80
        )
        
        self.plus_button = Button(
                                    label = "➕",
                                    width=60,
                                    height=30
                                   )
        
        def plus_button_clicked():
            self.value += self.stepsize 
            self.value_div.text = f"""
            <center><p> {self.variable_name} :  {self.value:.8E} {self.unit} </p></center>
                """
            
            
        self.plus_button.on_click(plus_button_clicked)
        
        
        self.minus_button = Button(
                                    label = "➖",
                                    width=60,
                                    height=30
                                   )
        
        def minus_button_clicked():
            self.value -= self.stepsize 
            self.value_div.text = f"""
            <center><p> {self.variable_name} :  {self.value:.8E} {self.unit} </p></center>
                """
            
        
        self.minus_button.on_click(minus_button_clicked)
        
        
        self.plus_button_step = Button(
                                    label = "➕",
                                    width=60,
                                    height=30
                                   )
        
        def plus_button_step_clicked():
            sig_fig = floor(self.stepsize / (10**floor(log10(self.stepsize))))
            if sig_fig == 1:
                self.stepsize *= 5
            if sig_fig == 5: 
                self.stepsize *= 2
            self.step_div.text = f"""
            <center><p> Stepsize :  {self.stepsize:.1E} {self.unit} </p></center>
                """
            
            
        self.plus_button_step.on_click(plus_button_step_clicked)
        
        
        self.minus_button_step = Button(
                                    label = "➖",
                                    width=60,
                                    height=30
                                   )
        
        def minus_button_step_clicked():
            sig_fig = floor(self.stepsize / (10**floor(log10(self.stepsize))))
            if sig_fig == 5:
                self.stepsize /= 5
            if sig_fig == 1: 
                self.stepsize /= 2
            self.step_div.text = f"""
            <center><p> Stepsize :  {self.stepsize:.1E} {self.unit} </p></center>
                """
        
        self.minus_button_step.on_click(minus_button_step_clicked)
        
        
        
         
        
        return row( column(self.plus_button,self.minus_button), self.value_div, column( self.plus_button_step, self.minus_button_step), self.step_div,)