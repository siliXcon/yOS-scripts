# SXAPI scripts

## How-to create an SXAPI gui
Example
 - Ensure you have the newest SWTools.
 - Download and install 'page' python GUI generator: http://page.sourceforge.net/
 - Design your GUI window in 'page' editor with drag&drop method.
 - Export the GUI and GUI support package (two Python files) from 'page'. Rename the exported GUI file to XXXX.sxp.
 - Add SXAPI interfacing code to the support file (XXXX_support.py). 'page' can generate a template for you, or use some of the examples.
 - Debug and tune your GUI from emGUI (file->open plugin). The stdout and stderr is directed to the emGUI's 'log' subwindow.
