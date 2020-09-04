# -----------------------------------------------------------
# UNDER DEVELOPMENT: DO NOT USE
# -----------------------------------------------------------
# Demonstrates how to plot a well path in 3D 
# Includes a method to plot data along that well path
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

import fractoolbox as ftb

#
# Import well survey data
#

dfsurvey = pd.read_csv('testdata-survey.csv')
print(dfsurvey.head(3))

#
# Define the casing shoe
#

# make a casing shoe df
data = {
    'shoe': ['production casing shoe'],
    'depth_mMDRF': [1000],
    }
casingshoe = pd.DataFrame(data)

# interpolate xyz for casing shoe using fractoolbox.xyzinterp
mDdat = casingshoe['depth_mMDRF']
mDsur = dfsurvey['depth_mMDRF']
xsur = dfsurvey['easting_m']
ysur = dfsurvey['northing_m']
zsur = dfsurvey['TVD_mRF']
dfxyz = ftb.xyzinterp(mDdat, mDsur, xsur, ysur, zsur) 
dfxyz.columns = ['depth_mMDRFx','northing_m','easting_m','TVD_mRF']
casingshoe = pd.concat([casingshoe,dfxyz], axis=1, join='inner')
casingshoe = casingshoe.drop(['depth_mMDRFx'],1)

# make df containing survey data for only the cased interval
'''
dfcased = dfsurvey[
    (dfsurvey.depth_mMDRF < casingshoe) & 
    (dfsurvey.depth_mMDRF > -0.1)
    ]
'''

#
# Work out the x & y limits for the plot
#

# To make the scale 1:1 for a single well:
#   Take the min X and Y values and add the well terminal depth (mVD)

# To make the scale 1:1 for multiple wells:
#   Take the min X and Y values and then add
#   either the plot depth or width, whichever is greater.
#       Calculate the maximum horizontal distance including all wells 
#       If it is greater that the terminal depth (mVD) of the deepest well, 
#           then use the maximum horizontal distance
#       Otherwise, use the terminal depth (mVD) of the deepest well

Xmin = dfsurvey['easting_m'].min()
Xmax = dfsurvey['easting_m'].max()
print('\n','Xmin =', Xmin,'Xmax =', Xmax,'\n')

Ymin = dfsurvey['northing_m'].min()
Ymax = dfsurvey['northing_m'].max()
print('Ymin =', Ymin,'Ymax =', Ymax,'\n')


# Force the rounding direction
def roundup(x):
    return int(math.ceil(x / 1000.0)) * 1000
def rounddown(x):
    return int(math.floor(x / 1000.0)) * 1000

YminR = rounddown(Ymin)
YmaxR = roundup(Ymax)

XminR = rounddown(Xmin)
XmaxR = roundup(Xmax)

Zshallowest = 0  # upperZlim use 0 if you want the collar at the top of the plot
Zdeepest = dfsurvey['TVD_mRF'].max() # set to total vertical depth

# ---------
# Make plot
# ---------

fig = plt.figure()
ax = plt.axes(projection='3d')

# plot well path
ax.plot(
    dfsurvey['easting_m'],
    dfsurvey['northing_m'],
    dfsurvey['TVD_mRF'],
    color='#8c510a',
    linewidth=1,
    )

# plot casing shoe
ax.scatter(
    casingshoe.iloc[0]['easting_m'],
    casingshoe.iloc[0]['northing_m'],
    casingshoe.iloc[0]['TVD_mRF'],
    s=40, color='k')

#
# Set axis limits
#

# Two options for setting xy lims
# ?????? describe

# Set x,y axis to make nice tidy plot
#ax.set_xlim(XminR,XmaxR)
#ax.set_ylim(YminR,YmaxR)


# Set x,y axis to make 1:1 scale with the depth
# and so the figure is centered on the production casing shoe
ax.set_xlim(
    casingshoe.iloc[0]['easting_m'] - Zdeepest / 2,
    casingshoe.iloc[0]['easting_m'] + Zdeepest / 2
    )

ax.set_ylim(
    casingshoe.iloc[0]['northing_m'] - Zdeepest / 2,
    casingshoe.iloc[0]['northing_m'] + Zdeepest / 2
    )

# Well plots are in TVD so the Z axis argumnets are plotted
# in the reverse of the cartesian coordiate system
ax.set_zlim(Zdeepest,Zshallowest)

#
# Format plot
# 

# get rid of axis tick labels
ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])
ax.zaxis.set_ticklabels([])

# set axes as three lines
[t.set_va('center') for t in ax.get_yticklabels()]
[t.set_ha('left') for t in ax.get_yticklabels()]
[t.set_va('center') for t in ax.get_xticklabels()]
[t.set_ha('right') for t in ax.get_xticklabels()]
[t.set_va('center') for t in ax.get_zticklabels()]
[t.set_ha('left') for t in ax.get_zticklabels()]

# make the panes transparent
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

# make the grid lines transparent
ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

# turns the grid and fill off
#ax.grid(False)
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
#ax.view_init(elev=90.,azim=-90.)       # plan view orented north 
#ax.view_init(elev=20,azim=-120.)       # oblique view 

plt.show()
