#!/usr/bin/env python3

## Time calibration of the channels of the PCB
from cmath import isnan, nan
from turtle import delay
import pandas as pd
import uproot
#import uproot3
import numpy as np
import track_time_calibration as ttc
from matplotlib import pyplot as plt
import Preparation as prep
import statistics as st
import Root_files_addition as rfa
import math as mt

c=30 ## speed of light
csc=17.526 ## speed of light in the fibre as cm/ns
length=192

# Channel that will be taken as a refence
ch_ref=63
t_id_ref=5
side='X'
delay=0

df=rfa.merger(['/home/ecal/Documents/scripts/Analysis/Data/10h/data_0000.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0001.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0002.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0003.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0004.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0005.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0006.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0007.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0008.root' ])
tracks=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Track_reconstruction/tracks.csv')## [indexx, indexy, truck-parameter, event_id]
tracks_id=tracks['track_id']
nb_tracks=len(tracks_id)

dsc_x_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dsc_X.csv')
dcal_x_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dcal_X.csv')
dsc_y_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dsc_Y.csv')
dcal_y_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dcal_Y.csv')

dsc_x=[ list(dsc_x_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]
dcal_x=[ list(dcal_x_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]

dsc_y=[ list(dsc_y_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]
dcal_y=[ list(dcal_y_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]

det_time_x=[[] for i in range(length)]
det_time_y=[[] for i in range(length)]
for track_id in range(nb_tracks):
    channels=df['tofpet_channel'].iloc[tracks_id[track_id]]
    tofpet=df['tofpet_id'].iloc[tracks_id[track_id]]
    t_stamp=df['timestamp'].iloc[tracks_id[track_id]]*6.25
    tr_param=tracks['track_param'].loc[track_id][1:-1].split(',')
    tr_param=[float(tr) for tr in tr_param]
    index_y=tracks['index_y'].loc[track_id][1:-1].split(',')
    index_y=[int(y) for y in index_y]
    index_x=tracks['index_x'].loc[track_id][1:-1].split(',')
    index_x=[int(x) for x in index_x]

    for ind in range(len(index_x)):
        index=index_x[ind]
        dsc_=dsc_x[track_id][ind]
        if not(np.isnan(dsc_)):
            dcal_=dcal_x[track_id][ind]
            chan=channels[index]
            tof_id=tofpet[index]
            t_ch=t_stamp[index]
            pos=ttc.position_in_array(chan,tof_id,'X')
            det_time_x[pos].append(t_ch-dsc_/csc-dcal_/c)

    for ind in range(len(index_y)):
        index=index_y[ind]
        dsc_=dsc_y[track_id][ind]
        if not(np.isnan(dsc_)):
            dcal_=dcal_y[track_id][ind]
            chan=channels[index]
            tof_id=tofpet[index]
            t_ch=t_stamp[index]
            pos=ttc.position_in_array(chan,tof_id,'Y')
            det_time_y[pos].append(t_ch-dsc_/csc-dcal_/c)

param_x=np.empty(192)
param_y=np.empty(192)
for i in range (192):
    param_x[i]=rfa.Gaussian_fit(det_time_x[i],i,'x')
    param_y[i]=rfa.Gaussian_fit(det_time_y[i],i,'y')
pd.DataFrame([param_x,param_y]).to_csv('Parameters_non_ref')
