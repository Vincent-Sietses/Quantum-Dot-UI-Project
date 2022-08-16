import numpy as np
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc


p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None

r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
           text_baseline="middle", text_align="center")

i = 0
print("oke")
ds = r.data_source

def callback():
    global i
    ds.data['x'].append(np.random.random()*70 + 15)
    ds.data['y'].append(np.random.random()*70 + 15)
    ds.data['text_color'].append(RdYlBu3[i%3])
    ds.data['text'].append(str(i))
    ds.trigger('data', ds.data, ds.data)
    i = i + 1

curdoc().add_root(column(p))
curdoc().add_periodic_callback(callback, 1000)

#show(p)