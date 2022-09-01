
<img  src="demo_screencap.PNG" align="center" width=20% height=20%>
<img  src="demo_screencap2.PNG" align="center" width=20% height=20%>

# Repo for storing code for UI Project for fast Quantum Dot measurements 

Project requires Python and Bokeh to be installed in an Anaconda environments

The QD UI Demo notebook contains all necessary information to use the LivePlotter module

Proves live Bokeh plotting, control of widgets and functions to interface with equipment


Obsolete : 
For Bokeh to open a browser tab with the interactive UI, run
``` bokeh serve --show <filename> ``` 

Write UI parameters in main.py, then run that file 

Important : make sure the files are being ran on the same OS as your browser (not through WSL etc.)


The Demo runs a complex quadratic with random noise which increases over time (useful for debug)