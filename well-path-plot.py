# -----------------------------------------------------------
# Demonstrates how to plot a well path in 3D 
#
# x is east, y is north, and z is total vertical depth (TVD)
#
# (C) 2020 Irene Wallis, Auckland, New Zealand 
# Email: irene@cubicearth.nz
# Released under a permissive open source licence Apache 2.0 
# https://choosealicense.com/licenses/apache-2.0/
# -----------------------------------------------------------

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import math

# https://github.com/ICWallis/fractoolbox
import fractoolbox as ftb

#
# Import well survey data as a pandas dataframe
#

dfsurvey = pd.read_csv('testdata-survey.csv')
#print(dfsurvey.head(2))

#
# Define the casing shoe pandas dataframe
#

data = {
    'shoe': ['production casing shoe'],
    'depth_mMDRF': [1000],
    }
dfcasingshoe = pd.DataFrame(data)

# Interpolate casing shoe xyz using fractoolbox.xyzinterp
mDdat = dfcasingshoe['depth_mMDRF']
mDsur = dfsurvey['depth_mMDRF']
xsur = dfsurvey['easting_m']
ysur = dfsurvey['northing_m']
zsur = dfsurvey['TVD_mRF']
dfxyz = ftb.xyzinterp(mDdat, mDsur, xsur, ysur, zsur) 
dfxyz.columns = ['depth_mMDRFx','easting_m','northing_m','TVD_mRF']
dfcasingshoe = pd.concat([dfcasingshoe,dfxyz], axis=1, join='inner')
dfcasingshoe = dfcasingshoe.drop(['depth_mMDRFx'],1)
#print(dfsurvey.head(2))

#
# Plot the data
#

fig = plt.figure()
ax = plt.axes(projection='3d')

# Plot well path
ax.plot(
    dfsurvey['easting_m'],
    dfsurvey['northing_m'],
    dfsurvey['TVD_mRF'],
    color='k',
    linewidth=1,
    )

# Plot casing shoe
ax.scatter(
    dfcasingshoe.iloc[0]['easting_m'],
    dfcasingshoe.iloc[0]['northing_m'],
    dfcasingshoe.iloc[0]['TVD_mRF'],
    s=40, color='k'
    )

#
# Set z axis limits
#
# This well plot method uses TVD so the Z axis arguments are plotted
# in the reverse of the cartesian coordinate system, which means that
# the values get larger in the downward direction

# Set the top of the plot: 
#   use 0 if you want the rig floor at the top of the plot
Zshallowest = 0

# Set the bottom of the plot: 
#   set here to the well terminal depth but could be set deeper
Zdeepest = dfsurvey['TVD_mRF'].max() 

ax.set_zlim(Zdeepest,Zshallowest)

#
# Set the xy axis limits
#
# Two methods are provided for setting xy lims
# Just comment out the one you don't want to use

# XYlims method 1: 
#   Plot centred on the well but not 1:1 scale
#   This method also forces rounding so the axis numbers plot nicely
'''
Xmin = dfsurvey['easting_m'].min()
Xmax = dfsurvey['easting_m'].max()
print('\n','Xmin =', Xmin,'Xmax =', Xmax,'\n')

Ymin = dfsurvey['northing_m'].min()
Ymax = dfsurvey['northing_m'].max()
print('Ymin =', Ymin,'Ymax =', Ymax,'\n')

def roundup(x):
    return int(math.ceil(x / 1000.0)) * 1000
def rounddown(x):
    return int(math.floor(x / 1000.0)) * 1000

YminR = rounddown(Ymin)
YmaxR = roundup(Ymax)

XminR = rounddown(Xmin)
XmaxR = roundup(Xmax)

ax.set_xlim(XminR,XmaxR)
ax.set_ylim(YminR,YmaxR)
'''

# XYlims method 2: 
#   Set x,y axis to make the plot scale 1:1 (horizontal to vertical)
#  
# To make the scale 1:1 for a single well:
#   Take the min X and Y values and add the well terminal depth (mVD)
#
# To make the scale 1:1 for multiple wells:
#   Take the min X and Y values that capture all the wells and then add
#   either the plot depth or width, whichever is greater.
#       Calculate the maximum horizontal distance including all wells 
#       If it is greater that the terminal depth (mVD) of the deepest well, 
#           then use the maximum horizontal distance
#       Otherwise, use the terminal depth (mVD) of the deepest well
#
# This method also arranges the figure so it is centered on the casing shoe
# Replacing dfcasingshoe with dfsurvey will arrange the figure so it's 
# centred on the rig floor

ax.set_xlim(
    dfcasingshoe.iloc[0]['easting_m'] - Zdeepest / 2,
    dfcasingshoe.iloc[0]['easting_m'] + Zdeepest / 2
    )

ax.set_ylim(
    dfcasingshoe.iloc[0]['northing_m'] - Zdeepest / 2,
    dfcasingshoe.iloc[0]['northing_m'] + Zdeepest / 2
    )

#
# Format plot
# 
# A rage of options for formatting the plot
# Just comment out the ones you don't want to use

# Get rid of axis tick labels
ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])
#ax.zaxis.set_ticklabels([])

# Set axes as three lines
[t.set_va('center') for t in ax.get_yticklabels()]
[t.set_ha('left') for t in ax.get_yticklabels()]
[t.set_va('center') for t in ax.get_xticklabels()]
[t.set_ha('right') for t in ax.get_xticklabels()]
[t.set_va('center') for t in ax.get_zticklabels()]
[t.set_ha('left') for t in ax.get_zticklabels()]

# Make the panes transparent
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

# Make all the grid lines transparent
#ax.grid(False)

# Make one set of grid lines transparent
ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
#ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

# Turn the grid and fill off
ax.xaxis.pane.set_edgecolor('black')
ax.yaxis.pane.set_edgecolor('black')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

#
# Set the start view for plt.show() or the exported view for plt.savefig()
#

#ax.view_init(elev=0.,azim=-90.)        # elevation view standing in the south and facing north 
#ax.view_init(elev=0.,azim=0.)          # elevation view standing in the west and facing east
ax.view_init(elev=0.,azim=-180.)        # elevation view standing in the east and facing west
#ax.view_init(elev=90.,azim=-90.)       # plan view oriented north 
#ax.view_init(elev=20,azim=-120.)       # oblique view 

plt.show()
