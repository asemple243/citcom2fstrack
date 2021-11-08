# convert_xyztolld
"""
Created on Fri Jun 11 13:49:44 2021

@author: Alana
"""
# input: csv form of citcoms results in x, y, z nondimensional format
# output: txt file of citcoms results in lat, long, depth coordinate system and dimensional 

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

#compute dimensional values
#xyz nd to meters
x = R0 * x_nd
y = R0 * y_nd
z = R0 * z_nd

x = pd.to_numeric(x)
y = pd.to_numeric(y)
z = pd.to_numeric(z)

# velo nd to m/s 
vx = Tdiff0/R0 * vx_nd
vy = Tdiff0/R0 * vy_nd
vz = Tdiff0/R0 * vz_nd

# convert xyz to polar lat lon and depth
# xyz should start in meters

a = 6378137.0 #in meters
b = 6356752.314245 #in meters

f = (a - b) / a
f_inv = 1.0 / f

e_sq = f * (2 - f)                       
eps = e_sq / (1.0 - e_sq)

p = np.sqrt((x * x + y * y))
#q = math.atan2((z * a), (p * b))
q = np.arctan2((z * a), (p * b))

sin_q = np.sin(q)
cos_q = np.cos(q)

sin_q_3 = sin_q * sin_q * sin_q
cos_q_3 = cos_q * cos_q * cos_q

phi = np.arctan2((z + eps * b * sin_q_3), (p - e_sq * a * cos_q_3))
lam = np.arctan2(y, x)

v = a / np.sqrt(1.0 - e_sq * np.sin(phi) * np.sin(phi))
d   = (p / np.cos(phi)) - v

lat = np.degrees(phi)
lon = np.degrees(lam)

#adding the axis=1 makes the concatenation horizontal, instead of vertical
lldata = pd.concat([ lat, lon, d, vx, vy, vz ],axis=1)
#setting index to False removes the extra column with all the index numbers
#setting header to None removes that first row of header names
lldata.to_csv("depths.txt",index=False,header=None)

