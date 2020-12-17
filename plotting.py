from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

# datetime formating to string
df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

# ColumnDataSource object to provide data to Bokeh
cds=ColumnDataSource(df)

# create figure object
f=figure(x_axis_type='datetime', height=200, width=500, title="Motion Graph")

# adjust plot attributes
f.yaxis.minor_tick_line_color=None
f.yaxis.ticker.desired_num_ticks=1

# setting up hover popup
hover=HoverTool(tooltips=[("Start","@Start_string"), ("End","@End_string")])
f.add_tools(hover)

# plotting a glyph
q=f.quad(left="Start", right="End", bottom=0, top=1, color="green", source=cds)

# create outputfile
output_file=("graph.html")

# display our graph
show(f)