#!/usr/bin/env python3
# Angular distribution of the incoming muon tracks


import numpy as np
import pandas as pd
import math as mt
from matplotlib import pyplot as plt
from random import sample, uniform

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

def uniform_proposal(x, delta=1.2740):
    x=0
    return np.random.uniform(x - delta, x + delta)

def metropolis_sampler(p, nsamples, proposal=uniform_proposal):
    x = 0 # start somewhere
    for i in range(nsamples):
        trial = proposal(x) # random neighbour from the proposal distribution
        acceptance = p(trial)/p(x)
        # accept the move conditionally
        if np.random.uniform() < acceptance:
            x = trial
            a = np.random.uniform(0,2*mt.pi)
            if(abs(mt.atan(mt.tan(a)*x)))<1.2740:
                yield mt.atan(mt.tan(a)*x)

p = lambda x: np.cos(x)**2
samples = list(metropolis_sampler(p, 1000000))
plt.figure()
x = np.arange(-1.2740, 1.2740, 0.01)
n,bin=np.histogram(samples,255)
#plt.figure()
min_=np.min(n)
n_corrected=(n-min_)*4.22803811
plt.plot(bin[:-1],n_corrected,linestyle='-',drawstyle='steps-post')
#plt.fill_between(x,n_corrected,step='pre',alpha=0.4)
plt.xlabel(r"Angle $\theta$ [rad]")
plt.ylabel(r"Number of tracks")
plt.grid("on")
#plt.savefig('/home/ecal/Documents/scripts/Analysis/Angular_study/Graphs/CosDistribution.png',dpi=300)


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
n,bin,patches=plt.hist(angles,50)
print(np.max(n))
plt.savefig('/home/ecal/Documents/scripts/Analysis/Angular_study/Graphs/SDistribution.png',dpi=600)
