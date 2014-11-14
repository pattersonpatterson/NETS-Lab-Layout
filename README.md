NETS-Lab-Layout
===============

Using python to create a dynamic map of the NETS lab.

INFO
----

The lab data is stored in the lab_data.xlsx spreadsheet (this filename is hard-coded into the script) in a 4 column table. Values can be added to the table ad infinitum without changes to the script unless:

* A new type of subsystem is added, in which case a new corresponding color must be added to the colormap section

* A new column is added, in which case the column name must be added to the source section and the reference must be made in the hovertool section in order for the data to come up on the tool-tip

Another limitation is the width of the lab: if the lab expands beyond R, the alphaconvert dictionary has to be updated.

# To Install

First run the command "pip -r Requirements.txt" to ensure that bokeh and pandas are installed.
