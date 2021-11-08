# -*- coding: utf-8 -*-

"""

@author: Alana
"""
# input: csv form of citcoms results in x, y, z nondimensional format
# output: txt file of citcoms results in x, y, z dimensional format (m & m/yr)

#########
import pandas as pd
import numpy as np
#import math
#import glob

# import xyz format data 
#### improve later to import all csvs OR use terminal to concatinate all csvs pre this step
xyzdat = pd.read_csv("veloTry2.2832008.csv")

# pull out columns to manipulate later
x_nd = xyzdat["Points:0"]
y_nd = xyzdat["Points:1"]
z_nd = xyzdat["Points:2"]

vx_nd = xyzdat["Velocity:0"]
vy_nd = xyzdat["Velocity:1"]
vz_nd = xyzdat["Velocity:2"]


#convert to dimensional data with eq from manual
# ref values from citcoms input.* file
R0 = 6371e3 # meters
Tdiff0 = 1e-6 # meters^2 / second
sinyr = 31536000.0 #seconds in 1 year

#compute dimensional values
#xyz nd to meters
x = R0 * x_nd
y = R0 * y_nd
z = R0 * z_nd

x = pd.to_numeric(x)
y = pd.to_numeric(y)
z = pd.to_numeric(z)

# velo nd to m/yr plus a multiplyer to get more motion in anisotropy calculations
vx = Tdiff0/R0 * vx_nd * sinyr * 10.
vy = Tdiff0/R0 * vy_nd * sinyr * 10.
vz = Tdiff0/R0 * vz_nd * sinyr * 10.

#adding the axis=1 makes the concatenation horizontal, instead of vertical
lldata = pd.concat([ x, y, z, vx, vy, vz ],axis=1)
#setting index to False removes the extra column with all the index numbers
#setting header to None removes that first row of header names
lldata.to_csv("velostep1-try1.csv",index=False,header=None)