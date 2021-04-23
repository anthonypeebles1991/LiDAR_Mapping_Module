# LiDAR_Mapping_Module
Original code for the LMM.  This includes the post processing code used to generate the LMM_DataViewer_GUI.exe, code on the Teensy 4.0, and the code that is on the RPi onboard the MRV.

## LMM
This file is the code that is running on the MRV's Raspberry Pi. It waits to see the LMM module handshake which is passed from the LMM to the Rpi via serial.  
Once the script sees the response "LMM" it will then run the script in a continuous loop.  The script simply keeps a counter for the number of clicks from the 
Hall sensors.  It sends the click count via the print function over serial to the LMM.  The LMM will read the value and log the current click count.

## RPLIDAR_v0.6.ino
This is the code that is on the Teensy 4.0 in the LMM box. In the setup it handles setting up the sensors and conducting the handshake with the MRV.
In the main loop it waits on a point from the LiDAR.  When a new point is ready it will grab the current heading from the BNO055 IMU, click count from the MRV,
and timestamp the data.  Then it logs the data collect to the on board SD card.

## Post Processing Code
### LIDAR_Processing_Tool.py
This is the main script for post processing the data.  In main you can point the data_path variable to the data directory and list the numbers of the 
data files to process.  The code will handle all of the necessray calculations for the transformation of the data into a 2D space.  This will create the 
raw data plot and the density plot for the data.

### LMM_DataViewer_GUI.py
This is the Graphical User Interface for the LMM.  This code uses the LIDAR_Processing_Tool to process the data and generate the plots.  This was also the 
script used to generate the LMM_DataViewer_GUI.exe.

### plottingTool.py
This is the script that sets the layout of the LMM_DataViewer_GUI.

### plottingTool.ui
This is the ui file for designing the GUI using the PyQt5 designer.  To use PyQt5 designer, if you have anaconda installed, simply open the anaconda prompt
and type `designer` then press enter.  This should run the designer interface.  Then you can open the .ui file to edit the GUI layout.  Once you are done with 
edits you can save the new .ui file and create the python file for the GUI.  To do this use the anaconda promt to navigate to the directory of the ui file.
Then enter the command `pyqt5 mylayout.ui -o mylayout.py` This will create the mylayout.py that you can then import to generate the GUI layout.
