# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 23:08:30 2021

@author: antho (Chad Peebles)
"""

import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D 
import os
import sys

CLICK_DISTANCE = 0.04026 # CONSTANT Meters per each hall sensor click
# CLICK_DISTANCE = 0.041
INCH_PER_METER = 39.37007874

# LIDAR Marker Plotting Params
LIDAR_MARKER_SIZE = 7
LIDAR_MARKER = '*'
LIDAR_COLOR = 'm'
LIDAR_COLOR_DEN = 'lime'

# LIDAR Data Plotting Params
LIDAR_POINT_SIZE = 1
LIDAR_POINT = '.'
LIDAR_POINT_COLOR = 'cornflowerblue'

# Density Params 
BIN_SIZE = 0.05

class LMM_DataViewer():
    def __init__(self, path_to_data):
        self.title = os.path.basename(path_to_data)
        
        self.distances1 = []
        self.lines1 = []
        self.annots1 = []
        self.startx1 = []
        self.starty1 = []
        self.endx1 = []
        self.endy1 = []
        
        self.distances = []
        self.lines = []
        self.annots = []
        self.startx = []
        self.starty = []
        self.endx = []
        self.endy = []
        
        self.total_time = 0
        self.total_distance = 0
        self.total_points = 0
        
        
        self.shift_key_held_den = False
        self.shift_key_held_data = False
        
        self.fig_den = plt.figure()
        self.fig_den.set_size_inches(10,10)
        self.fig_den.show()
        self.ax_den = self.fig_den.add_subplot(111)
        
        
        self.fig_data = plt.figure()
        self.fig_data.set_size_inches(10,10)
        self.fig_data.show()
        self.ax_data = self.fig_data.add_subplot(111)
        # self.ax_data.grid()
        
        self.df = self.process_data(path_to_data)
        
    def distance_midpoint(self, x1, x2, y1, y2):
        """
        return the distance and midpoint between two points
        """
        dis = (np.sqrt((x1 - x2)**2 + (y1 - y2)**2))
        midx, midy = ((x1+x2)/2), ((y1+y2)/2)
        return dis, midx, midy
   
    def m_to_feet_inch(self, meters):
        inches = meters * INCH_PER_METER
        feet = math.floor(inches/12)
        inch_left = inches - (feet*12)
        return feet, inch_left
    
    def on_press_den(self, event):
        sys.stdout.flush()
        if event.key == 'd':
            
            x, y = event.xdata, event.ydata
            if (len(self.startx) == len(self.endx)):
                self.startx.append(x)
                self.starty.append(y)
            else:
                self.endx.append(x)
                self.endy.append(y)
                sx = self.startx[-1]
                ex = self.endx[-1]
                sy = self.starty[-1]
                ey = self.endy[-1]
                
                # Get distance and midpoint
                dis, midx, midy = self.distance_midpoint(sx, ex, sy, ey)
                self.distances.append(dis)
                
                # Add line
                line = Line2D([sx, ex], [sy, ey], linestyle='-.',color = 'r', 
                              marker='o', markerfacecolor='limegreen')
                self.lines.append(self.ax_den.add_line(line))
                
                # Add measurement
                feet, inches = self.m_to_feet_inch(dis)
                text = '{0:0.4f}[m]\n{1:d}\' {2:0.2f}"'.format(dis, feet, inches)
                annot = self.ax_den.text(midx+.05,midy+.05,text,color='w',
                                         fontsize = 'small',fontweight='demi',
                                         bbox=dict(boxstyle="square",
                                                              ec=('k'),
                                                              fc=('k')))
                self.annots.append(annot)
                self.fig_den.canvas.draw()
            
            
        if event.key == 'shift':
            self.shift_key_held_den = True
            
        if self.shift_key_held_den and event.key == 'Z':
            self.ax_den.lines.remove(self.lines[-1])
            annot = self.annots.pop()
            annot.remove()
            self.distances.pop()
            self.lines.pop()
            
            self.startx.pop()
            self.starty.pop()
            self.endx.pop()
            self.endy.pop()
            self.fig_den.canvas.draw()
            
    def on_release_den(self, event):
        sys.stdout.flush()
        if event.key == 'shift':
            self.shift_key_held_den = False
            
    def on_press_data(self, event):
        sys.stdout.flush()
        if event.key == 'd':
            x, y = event.xdata, event.ydata
            if (len(self.startx1) == len(self.endx1)):
                self.startx1.append(x)
                self.starty1.append(y)
            else:
                self.endx1.append(x)
                self.endy1.append(y)
                sx = self.startx1[-1]
                ex = self.endx1[-1]
                sy = self.starty1[-1]
                ey = self.endy1[-1]
                
                # Get distance and midpoint
                dis, midx, midy = self.distance_midpoint(sx, ex, sy, ey)
                self.distances1.append(dis)
                
                # Add line
                line = Line2D([sx, ex], [sy, ey], linestyle='-.',color = 'r', 
                              marker='o', markerfacecolor='limegreen')
                self.lines1.append(self.ax_data.add_line(line))
                
                # Add measurement
                feet, inches = self.m_to_feet_inch(dis)
                text = '{0:0.4f}[m]\n{1:d}\' {2:0.2f}"'.format(dis, feet, inches)
                annot = self.ax_data.text(midx+.05,midy+.05,text,color='w',
                                         fontsize = 'small',fontweight='demi',
                                         bbox=dict(boxstyle="square",
                                                              ec=('k'),
                                                              fc=('k')))
                self.annots1.append(annot)
                self.fig_data.canvas.draw()
            
        if event.key == 'shift':
            self.shift_key_held_data = True
            
        if self.shift_key_held_data and event.key == 'Z':
            self.ax_data.lines.remove(self.lines1[-1])
            annot = self.annots1.pop()
            annot.remove()
            self.distances1.pop()
            self.lines1.pop()
            self.startx1.pop()
            self.starty1.pop()
            self.endx1.pop()
            self.endy1.pop()
            self.fig_data.canvas.draw()
            
            
    def on_release_data(self, event):
        sys.stdout.flush()
        if event.key == 'shift':
            self.shift_key_held_data = False
    
    
    def plot_data(self, df):
        print('\tIn plot_data()')
        ##########################################################################
        ###########                  Make Density Plot                 ###########
        ##########################################################################
        # Find max dist between either axis
        num_bins = int(round((df['lp_x'].max() - df['lp_x'].min())/BIN_SIZE))
        
        title = self.title + ' Density of Data'
        self.ax_den.set_title(title)
        self.ax_den.set_xlabel('X [m]')
        self.ax_den.set_ylabel('Y [m]')
        print('\tTrying Hex bin density plot')
        self.ax_den.hexbin(df['lp_x'], df['lp_y'],cmap='plasma', bins = 'log',gridsize=num_bins)
        
        print('\tDone with hex bin density\n\tPlotting MRV locations')
        
        self.ax_den.plot(df['mrv_x'], df['mrv_y'], c=LIDAR_COLOR_DEN, 
                          label='MRV Position', markersize=LIDAR_MARKER_SIZE)
        
        chunk = len(df) * .001
        skip_num_rows = int(len(df)/chunk)
        tempdf = df[df.index % skip_num_rows == 0]                           
        x0 = tempdf['mrv_x'].iloc[range(len(tempdf['mrv_x'])-1)].values
        x1 = tempdf['mrv_x'].iloc[range(1,len(tempdf['mrv_x']))].values
        y0 = tempdf['mrv_y'].iloc[range(len(tempdf['mrv_y'])-1)].values
        y1 = tempdf['mrv_y'].iloc[range(1,len(tempdf['mrv_y']))].values
        xpos = (x0+x1)/2
        ypos = (y0+y1)/2
        xdir = x1-x0
        ydir = y1-y0
        
        # Plot direction arrows
        for X,Y,dX,dY in zip(xpos, ypos, xdir, ydir):
            self.ax_den.annotate("", xytext=(X,Y),xy=(X+0.001*dX,Y+0.001*dY), 
                                  arrowprops=dict(arrowstyle="->", color='r'), size = 10)
            
        self.fig_den.canvas.mpl_connect('key_press_event', self.on_press_den)
        self.fig_den.canvas.mpl_connect('key_release_event', self.on_release_den)
        
        self.ax_den.set_aspect('equal', adjustable='box')                      ################### added
        
        ##########################################################################
        ###########                    Make Data Plot                  ###########
        ##########################################################################
        # plt.style.use('ggplot')
        # fig, ax = plt.subplots()
        # fig.set_size_inches(8,8)
        self.ax_data.set_xlabel('X [m]')
        self.ax_data.set_ylabel('Y [m]')
        self.ax_data.set_title(self.title)
        
        self.ax_data.plot(df['lp_x'], df['lp_y'], LIDAR_POINT, markersize=LIDAR_POINT_SIZE, 
                color=LIDAR_POINT_COLOR, label='LIDAR data points')   
        
        self.ax_data.plot(df['mrv_x'], df['mrv_y'], c=LIDAR_COLOR, 
                          label='MRV Position', markersize=LIDAR_MARKER_SIZE)
        
        self.ax_data.set_aspect('equal', adjustable='box')                      ################### added
        
        chunk = len(df) * .001
        skip_num_rows = int(len(df)/chunk)
        tempdf = df[df.index % skip_num_rows == 0]                   
        x0 = tempdf['mrv_x'].iloc[range(len(tempdf['mrv_x'])-1)].values
        x1 = tempdf['mrv_x'].iloc[range(1,len(tempdf['mrv_x']))].values
        y0 = tempdf['mrv_y'].iloc[range(len(tempdf['mrv_y'])-1)].values
        y1 = tempdf['mrv_y'].iloc[range(1,len(tempdf['mrv_y']))].values
        xpos = (x0+x1)/2
        ypos = (y0+y1)/2
        xdir = x1-x0
        ydir = y1-y0
        for X,Y,dX,dY in zip(xpos, ypos, xdir, ydir):
            self.ax_data.annotate("", xytext=(X,Y),xy=(X+0.001*dX,Y+0.001*dY), 
                                  arrowprops=dict(arrowstyle="->", color='k'), size = 20)
        
        # Plot start and end arrows
        xstart = df['mrv_x'].iloc[0]
        ystart = df['mrv_y'].iloc[0]
        xend = df['mrv_x'].iloc[-1]
        yend = df['mrv_y'].iloc[-1]
        
        off = 27
        width = 3
        offset = off
        
        # START point arrow
        bbox = dict(boxstyle="round", fc="limegreen")
        arrowprops = dict(
            arrowstyle = "->", color = 'limegreen', linewidth = width,
            connectionstyle = "angle3,angleA=90,angleB=0")
        
        
        self.ax_data.annotate('Start',
                    (xstart, ystart), xytext=(-2*offset, offset), textcoords='offset points',
                    bbox=bbox, arrowprops=arrowprops)
        
        # END point arrow
        offset = -off
        bbox = dict(boxstyle="round", fc="r")
        arrowprops = dict(
            arrowstyle = "->", color = 'r', linewidth = width,
            connectionstyle = "angle3,angleA=-180,angleB=-90")
        
        self.ax_data.annotate('End',
                    (xend, yend), xytext=(-2*offset, offset), textcoords='offset points',
                    bbox=bbox, arrowprops=arrowprops)
            
        
        self.ax_data.legend()
        
        self.fig_data.canvas.mpl_connect('key_press_event', self.on_press_data)
        self.fig_data.canvas.mpl_connect('key_release_event', self.on_release_data)
        
        # plt.style.use('default')
        return 
    
    def process_data(self, path):
        df = pd.read_csv(path)
        
        df.columns = df.columns.str.replace(' ', '')
        df.sort_values(by='Time', inplace = True)
        df = df[df['Quality']>=15]                                              # Filter out bad Quality
        
        df['Seconds'] = df['Time'] * (10**-6)                                   # Get time in seconds
        df['dt'] = np.diff(df['Seconds'], prepend=df['Seconds'].iloc[0])        # Get delta time 
        
        
        
        ##########################################################################
        ###########               Handling MRV's rotation              ###########
        ##########################################################################
        df['Heading_Shift'] = df['Heading'] - df['Heading'].iloc[0]             # Heading shift from initial heading @ t=0
        
        df['Corrected_Az'] = df['Azimuth'] + df['Heading_Shift']                # Correct LIDAR azimuths to acount for
                                                                                # shifts in the MRV heading.
        
        df['Range'] = df['Distance']*.001                                       # Distance [mm] /1000 to get in meters.
        
        df['lp_x'] = df['Range']*np.cos(np.deg2rad(df['Corrected_Az']))         # Decompose X from az and range
        df['lp_y'] = df['Range']*np.sin(np.deg2rad(df['Corrected_Az']))         # Decompose Y from az and range
        ##########################################################################
        #_________________________________________________________________________
    
        ##########################################################################
        ###########             Handling MRV's displacement            ###########
        ##########################################################################
        
        df['d_Clicks'] = np.diff(df['Clicks'], prepend=0)                       # Get how many clicks moved
        df['d_distance'] = df['d_Clicks']*CLICK_DISTANCE                        # Get distance traveled at each time step
        
        df['mrv_dx'] = df['d_distance']*np.cos(np.deg2rad(df['Heading']))       # Get MRV's change in X at each time step
        df['mrv_dy'] = df['d_distance']*np.sin(np.deg2rad(df['Heading']))       # Get MRV's change in Y at each time step
        
        df['mrv_x'] = np.cumsum(df['mrv_dx'])                                   # Get MRV's cumulative displacement in X
        df['mrv_y'] = -np.cumsum(df['mrv_dy'])                                  # Get MRV's cumulative displacement in Y
        
        df['lp_x'] += df['mrv_x']                                               # Adjust LIDAR points reference to MRV X location
        df['lp_y'] -= df['mrv_y']   
        df['lp_y'] = -df['lp_y']                                                # Adjust LIDAR points reference to MRV Y location
        ##########################################################################
        #_________________________________________________________________________
        
        self.total_time = df['Seconds'].iloc[-1] - df['Seconds'].iloc[0]
        self.total_points = len(df)
        self.total_distance = df['d_distance'].sum()
        
        print('\tTrying to plot data')
        self.plot_data(df)
        return df

if __name__ == '__main__':
    
    data_path = r'\Sample Data Plotting\_data'
    data_nums_to_run = [180]
    
    ref = []
    for num in data_nums_to_run:
        filename = 'DATA_'+str(num)+'.txt'
        data_file = os.path.join(data_path, filename)
        
        LMM_view = LMM_DataViewer(data_file)
        ref.append(LMM_view)


























