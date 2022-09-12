#!/usr/bin/env python3
# Angular distribution of the incoming muon tracks


import numpy as np
import pandas as pd
import sys
import math as mt
from matplotlib import pyplot as plt

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

tracks=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Track_reconstruction/tracks.csv')


track_id=tracks['track_id']

nb_tracks=len(track_id)
angles=np.zeros(nb_tracks)
for track_id1 in range(len(track_id)):
    tr_param=tracks['track_param'].loc[track_id1][1:-1].split(',')
    tr_param=[float(tr) for tr in tr_param]
    x0=tr_param[0]
    y0=tr_param[2]
    x=-tr_param[1]+x0
    y=-tr_param[3]+y0
    z=8
    norm=mt.sqrt((x-x0)**2+(y-y0)**2+z**2)
    angles[track_id1]=(mt.acos((z/norm)))
print(nb_tracks)
#print(len(np.argwhere(angles<=mt.pi) & (angles>=1.56)))
plt.figure()
n,bin,patches=plt.hist(angles,50)
print(np.max(n))
plt.xlabel(r"Angles $\theta$ [rad]")
plt.ylabel(r"Number of tracks")
plt.grid()
plt.show()
plt.savefig('/home/ecal/Documents/scripts/Analysis/Angular_study/Graphs/Distribution.png',dpi=600)
