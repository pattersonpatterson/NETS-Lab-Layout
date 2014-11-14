# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 15:31:34 2014

@author: derpson
"""

# imports
import string
import pandas as pd
import bokeh.plotting as bk
from bokeh.objects import HoverTool, ColumnDataSource
from collections import OrderedDict


# Read data from Excel spreadsheet lab_data.xlsx
# Use pandas to organize data.table
xl = pd.ExcelFile("lab_data.xlsx")
df = xl.parse(sheetname="ESS-Lab")

# Output to html
bk.output_file("ESS-layout.html", title="ESS Layout Sketch")

# Convert lab position to grid position
keys = []
values = []
for alph in reversed(string.uppercase[:18]):
    keys.append(alph)
for num in range(1,19):
    values.append(num)

#### create dictionary of R-A:1-18
alphaconvert = dict(zip(keys,values))
del keys, values

#### split out lab location into xpos and ypos
df['xpos'] = df.labLocation.str.split("-").str[0]
df['ypos'] = df.labLocation.str.split("-").str[1]

#### set data types
df['ypos'] = df.ypos.astype(int)
df['cabinetName'] = df.cabinetName.astype(str)
df['equipment'] = df.equipment.astype(str)
df['phone'] = df.phone.astype(str)

#### replace xpos with alphaconversion
for key,val in alphaconvert.iteritems():
    df['xpos'][df.xpos==key] = val

# Set x-y ranges
x_range = [str(x) for x in range(1,19)]
y_range = [str(y) for y in range(1,36)]

# Map fill colors to subsystem type
colormap= {
    'ES1':'#ECBBAF',
    'BS1':'#D6C7CA',
    'CAT':'#85C680',
    'Workstation': '#79AED2',
    'Storage':'#FED9A9',
    'Future':'#D6D6B8',
    'SL1':'#BF6F32'
}

# Insert data into ColumnDataSource
source = ColumnDataSource(
    data=dict(
        posx=[str(x) for x in df['xpos']],
        posy=[str(y) for y in df['ypos']],
        text_locy=[str(y)+":0.75" for y in df['ypos']],
        text_namey=[str(y)+":0.3" for y in df['ypos']],
        text_suby=[str(y)+"0.15" for y in df['ypos']],
        name = df['cabinetName'],
        loc = df['labLocation'],
        sub = df['subsystem'],
        equip = df['equipment'],
        phone = df['phone'],
        color_type = [colormap[str(x)] for x in df['subsystem']]
    )
)

# hold() to put all glyphs on the same graph
bk.hold()
# Make a rect glyph for each element of data
bk.rect("posx", "posy", 0.9, 0.9, source=source,
    x_range=x_range, y_range=y_range,
    fill_alpha=0.6, color="color_type",
    tools="resize,hover,previewsave,ywheel_zoom", title="ESS Lab Layout",
    plot_width=1200
)

# Use text_props = dict to set properties of text elements
text_props = {
    "source": source,
    "angle": 0,
    "color": "black",
    "text_align": "center",
    "text_baseline": "middle"
}

# Make a text glyph for each rect glyph to show the cabinet names and locations
bk.text(x=dict(field="posx", units="data"),
     y=dict(field="text_locy", units="data"),
     text=dict(field="loc", units="data"),
     text_font_style="bold", text_font_size="12pt", **text_props)

bk.text(x=dict(field="posx", units="data"),
     y=dict(field="text_namey", units="data"),
     text=dict(field="name", units="data"),
     text_font_style="bold", text_font_size="9pt", **text_props)

bk.text(x=dict(field="posx", units="data"),
     y=dict(field="text_suby", units="data"),
     text=dict(field="sub", units="data"),
     text_font_style="bold", text_font_size="9pt", **text_props)

# turn off grid lines
bk.grid().grid_line_color = None
# Add hovertool to show equipment in tooltips
hover = bk.curplot().select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
    ("name", "@name"),
    ("subsystem", "@sub"),
    ("equipment","@equip"),
    ("phone","@phone")
])

# Show the graph
bk.show()
