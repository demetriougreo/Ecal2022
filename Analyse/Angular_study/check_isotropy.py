#!/usr/bin/env python3
## Check that the system is indeed isotropic under rotations around the z axis
from cmath import pi
import numpy as np
import pandas as pd
import sys
import math as mt
from matplotlib import pyplot as plt
import time

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})
# for Palatino and other serif fonts use:
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"],
})
# It's also possible to use the reduced notation by directly setting font.family:
plt.rcParams.update({
  "text.usetex": True,
  "font.family": "Helvetica"
})

tracks = pd.read_csv('/home/ecal/Documents/scripts/Analysis/Track_reconstruction/tracks.csv')
#tracks2 = pd.read_csv('/home/ecal/Documents/scripts/Analysis/Track_reconstruction/tracks-rainy.csv')

tracks_id=tracks['track_id']
#tracks2_id=tracks2['track_id']
#nb_tracks=len(tracks_id)+len(tracks2_id)
angles=np.zeros(len(tracks_id))
for track_id1 in range(len(tracks_id)):
    phi=0
    tr_param=tracks['track_param'].loc[track_id1][1:-1].split(',')
    tr_param=[float(tr) for tr in tr_param]
    x0=tr_param[0]
    y0=tr_param[2]
    x=-tr_param[1]+x0
    y=-tr_param[3]+y0
    z=8
    dx=x0-x
    dy=y0-y
    if dx>0:
        phi=mt.atan(dy/dx)
    elif dx<0 and dy>=0:
        phi=mt.atan(dy/dx)+mt.pi
    elif dx<0 and dy<0:
        phi=mt.atan(dy/dx)-mt.pi
    elif dx==0 and dy>0:
        phi=mt.pi/2
    elif dx==0 and dy<0:
        phi=-mt.pi/2
    angles[track_id1]=phi
    print(dx)
    print(dy)
    print(angles[track_id1])

pd.DataFrame(angles).to_csv("Angles")
plt.figure()

h, bins,_ = plt.hist(angles,100)
plt.xlabel(r"Angles $\theta$ [rad]")
plt.ylabel(r"Number of tracks")
plt.grid()
plt.show()
plt.savefig('/home/ecal/Documents/scripts/Analysis/Angular_study/Graphs/Isotropy.png',dpi=600)
