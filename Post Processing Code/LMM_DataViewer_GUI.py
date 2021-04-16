# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 13:30:31 2021

@author: antho
"""
from plottingTool import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import LIDAR_Processing_Tool as LPT




class ApplicationWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/Images/LMMicon.ico')) # The colon must be there
        
        self.input_file = ''
        self.LMM_dataviews = []
        self.LMM_header = 'Time,Heading,Clicks,Azimuth,Distance,Quality\n'
        self.connectSignals()
        self.enablePlot(False)
        self.ui.info_box.append('Select a new data file with the "Browse to LiDAR data file" button.')
        
    def connectSignals(self):
        self.ui.browse_button.clicked.connect(self.openFileNameDialog)        
        self.ui.plot_button.clicked.connect(self.plotData)
        
    def openFileNameDialog(self, obj):
            options = QtWidgets.QFileDialog.Options()
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Open File", "", ";All Files (*)", options=options)
            self.input_file = fileName
            self.ui.filename_label.setText(os.path.basename(self.input_file))
            try:
                
                with open(self.input_file, 'r') as buf:
                    header = buf.readline()
                    if header == self.LMM_header:
                        self.enablePlot(True)
                        self.ui.plot_button.setEnabled(True)
                        self.onFileSelection()
                    else:
                        self.enablePlot(False)
                        self.printFileTypeError(header)
            except:
                self.enablePlot(False)
                self.printFileTypeError()
    def enablePlot(self, on):
        if on:
            self.ui.plot_button.setEnabled(True)
            self.ui.plot_button.setStyleSheet("background:lightgreen; font:bold 14px")
        else:
            self.ui.plot_button.setEnabled(False)
            self.ui.plot_button.setStyleSheet("background:crimson; font:bold 14px")
                
    def onFileSelection(self):
        self.ui.info_box.append('File Selected. Click the Plot button to view.')
        self.ui.info_box.append('Or Select a new data file with the "Browse to LiDAR data file" button.')
        
    def plotData(self):
        print('Creating LMM_DataViewer')
        LMM_view = LPT.LMM_DataViewer(self.input_file)
        print('Done Creating LMM_DataViewer')
        self.LMM_dataviews.append(LMM_view)
        
        self.printDataStats(LMM_view)
        self.printPlotterInfo()
        
    def printDataStats(self, LMM_view):
        self.ui.info_box.append('\n                ' + os.path.basename(self.input_file))
        time_of_collect = LMM_view.total_time
        distance_traveled = LMM_view.total_distance
        num_data_points = LMM_view.total_points
        time = '    Total Time of Data:\t' + str(time_of_collect) + '[s]\n'
        dis = '    Distance traveled by MRV:\t' + str(distance_traveled) + '[m]\n'
        points = '    Total number of data points:\t' + str(num_data_points) 
        self.ui.info_box.append('\n           DATA INFO')
        self.ui.info_box.append(time + dis + points)
        
        
        
    def printPlotterInfo(self):
        self.ui.info_box.append('\n           PLOTTER MEASURE TOOL')
        message = '''
    To mark a distance (point to point):
        1. Make sure plot is active (click on it)
        2. Hover over start point and press d
        3. Hover over end point and press d
                        
    To Remove measurement lines:
        1. Make sure plot is active (click on it)
        2. Press shift+z
                    '''
        self.ui.info_box.append(message)
        self.ui.info_box.append('*'*30+'\n')
        self.ui.info_box.append('\nPress "Plot" to plot again or select a new data file.')
        return
    
    def printFileTypeError(self, header=None):
        self.ui.info_box.append('File is not a LMM data file!!!\n')
        if header:
            good = self.LMM_header.strip()
            bad = header.strip()
            self.ui.info_box.append('First Line of LMM data should be : \t->'+good+'<-')
            self.ui.info_box.append('First line read was: \t\t->' + bad + '<-')
            self.ui.info_box.append('We cannot process data without the proper header.')
        self.ui.info_box.append('*'*30+'\n')
        self.ui.info_box.append('Use the "Browse to LiDAR data file" button to select a LMM data file...')
        
        
if __name__ == '__main__':
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QtCore.QCoreApplication.instance()
    
    if app is None:
        app = QApplication([])
        
    app.lastWindowClosed.connect(app.quit)
    app.setStyle('Fusion')
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())
     
       
        
      