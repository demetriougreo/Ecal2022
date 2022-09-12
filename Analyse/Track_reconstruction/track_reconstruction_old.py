#!/usr/bin/env python3
# Contains the functions used to determine the tracks of a signal. Doesn't contains any filter, chi2 function
# Can be used to determine if the computed track fit with the data 
# Use Hough transfomations on each side of the calorimeter to determine the parameters of the projection of the 
# track. Having the projections of the track make it easy to reconstruct the 3D track 
import numpy as np
import pandas as pd
import sys
from itertools import combinations
from matplotlib import pyplot as plt



def same_layer(channels,tofpet_id):
    filepath="/home/ecal/Documents/scripts/Analysis/ECAL_SiPM_mapping.xlsx" # Filepath to mapping of the SiPM  to the position on the PCB
    position=pd.read_excel(filepath)
    channel=position['Channel']
    TOFPET=position['TOFPET']
    size=len(channels)
    data2_internal=tofpet_id%2
    layer=np.zeros((size,),dtype=int)
    for i in range(size):
        layer[i]=position.loc[(channel== channels[i]) & (TOFPET == data2_internal[i])]['Layer']
        if tofpet_id[i] == 4 or tofpet_id[i] == 5 or tofpet_id[i] == 6 or tofpet_id[i] == 7:
            layer[i]=layer[i]+4
    return layer

# Takes out all the hits that happened on the same layer
def good_pairs(data,i):
  test=np.argwhere(data==i)
  return test

# Checks that a & b belongs to different sides. a & b are tofpet_ids
def check_sides(a,b):
    if(a==(0|1|4|5)):
        sidea=0
    else:
        sidea=1
    if(b==(0|1|4|5)):
        sideb=int(0)
    else:
        sideb=int(1)
    if sideb == sidea:
        return True
    else:
        return False

# Check that a is tofpet on the x side of the calorimeter
def is_sidex(a):
    if(a==0 or a==1 or a==4 or a==5):
        return 0
    else:
        return 1

# Determine the (X,Z) or (Y,Z) coordinate of a hits, depending on what tofpet_id is entered. Triplet=[channel,t_id,layer]
def correction2D(triplet):
    filepath="/home/ecal/Documents/scripts/Analysis/ECAL_SiPM_mapping.xlsx" # Filepath to mapping of the SiPM  to the position on the PCB
    corr = np.array([1, 1])
    position = pd.read_excel(filepath)
    channel = position['Channel']
    TOFPET = position['TOFPET']
    corr[0] = position.loc[(channel == triplet[0]) & (TOFPET == (triplet[1] % 2))]['Bar']
    corr[1] = triplet[2]
    return corr

# i j indicate which hit we are looking at, t is the angle at which we are looking for an overlap and x0 is the dataframe with the x0
# as a function of the angle t
def overlap(i,j,t,x0):
    if (x0['xu'][i][t]>=x0['xu'][j][t] and x0['xd'][i][t]<=x0['xu'][j][t]) or x0['xu'][j][t]>=x0['xu'][i][t] and x0['xd'][j][t]<=x0['xu'][i][t]:
        ol=True
    else:
        ol=False
    return ol

## Looks how many hits overlap at a certain angle t. Return the the hits index that overlap, the number of overlaping
# and the boundaries, boundaries are the extremal x that belongs to the overlap region
def max_overlap (x0,t):
    indices=[]
    boundaries=[0,0]
    length=0
    n_hits=len(x0['xu'])
    for i in range(n_hits-1):
        indices_i=[i]
        for j in range(i+1,n_hits):
            if all([overlap(k,j,t,x0) for k in indices_i]):
                indices_i=np.append(indices_i,j)
        if len(indices_i)>length:
            indices=indices_i
            length=len(indices)
    if not ([x0['xu'][i][t] for i in indices]):
        return []
    else:
        boundaries[0]=min([x0['xu'][i][t] for i in indices])
        boundaries[1]=max([x0['xd'][i][t] for i in indices])
    return indices,length,boundaries


## This function provide the parameters x0 (or y0 depending on which hits we provide) and tx the angle of the trac
def tracks(hits):
    n_points=100
    max=5
    tneg=np.linspace(-max,0,n_points) # region over which we want to look for the angle
    tpos=np.linspace(0,max,n_points)
    n_hits=len(hits)
    x0=pd.DataFrame(columns=['xu','xd'])
    x0['xu']=[np.zeros(2*n_points) for i in range(n_hits)]
    x0['xd']=[np.zeros(2*n_points) for i in range(n_hits)]
    for hit in range(0,n_hits):
        x0['xu'][hit][0:n_points]=hits[hit][0]+1-(hits[hit][1]-8)*tneg # Up boundary for x0 for hit number hit in region t<0
        x0['xu'][hit][n_points:2*n_points]=hits[hit][0]+1-(hits[hit][1]-9)*tpos # Up boundary for x0 for hit number hit in region t>0
        x0['xd'][hit][0:n_points]=hits[hit][0]-(hits[hit][1]-9)*tneg
        x0['xd'][hit][n_points:2*n_points]=hits[hit][0]-(hits[hit][1]-8)*tpos
        #### Display of the parameter the parameter space
        color_=['b','crimson','k','r','c','crimson','m','darkorange','purple']
        plt.plot(tneg,x0['xu'][hit][0:n_points],color=color_[hit],ls='-',lw=1,fillstyle='none')
        plt.plot(tpos,x0['xu'][hit][n_points:2*n_points],color=color_[hit],ls='-',lw=1,fillstyle='none')
        plt.plot(tneg,x0['xd'][hit][0:n_points],color=color_[hit],ls='-',lw=1,fillstyle='none')
        plt.plot(tpos,x0['xd'][hit][n_points:2*n_points],color=color_[hit],ls='-',lw=1,fillstyle='none')
    plt.show()

    ##### Now have to find the region of overlap

    T=np.append(tneg,tpos)
    t_overlap=[[] for i in range(2*n_points)]
    boundaries=[[] for i in range(2*n_points)]
    t_max=0
    overlap=0
    for t in range(2*n_points):
        a=0
        t_overlap[t],a, boundaries[t]=max_overlap(x0,t)
        if a>overlap:
            t_max=t
            overlap=a
    t_max_overlap=[T[t] for t in range(2*n_points) if len(t_overlap[t])==overlap]
    min_max_overlap=[boundaries[t] for t in range(2*n_points) if len(t_overlap[t])==overlap]
    index_=t_overlap[t_max]
    t=np.mean(t_max_overlap)
    out=np.mean([np.mean(ov) for ov in min_max_overlap])
    return out, t, index_

def chi_2(Hits,track,index_):
    dof=1
    critX=3.841
    expected=[track[Hits[i][1]-1][0] for i in index_]
    X2=sum([(Hits[index_[i]][0]-expected[i])**2/expected[i] for i in range(len(index_))])
    if X2> critX:
        return False
    else:
        return True
