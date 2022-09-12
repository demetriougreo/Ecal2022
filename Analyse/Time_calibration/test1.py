#!/usr/bin/env python3

## Time calibration of the channels of the PCB
import time
import pandas as pd
import uproot
import uproot3
import numpy as np
import track_time_calibration as ttc
import Preparation as prep
import statistics as st
import functions_ttc as ftc
import matplotlib.pyplot as plt
import Root_files_addition as rfa

c=30 ## speed of light
csc=17.526 ## speed of light in the fibre as cm/ns
length=192

# Channel that will be taken as a refence
ch_ref=62
t_id_ref=4
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


a=pd.read_csv('electronic_delay_x.csv')
electronic_delay_x=np.array(a[a.columns[1]])
a=pd.read_csv('electronic_delay_y.csv')
electronic_delay_y=np.array(a[a.columns[1]])
a=pd.read_csv('t_entries.csv')
t_entries=np.array(a[a.columns[1]])
det_time_x=[[] for i in range(length)]
det_time_y=[[] for i in range(length)]
for track_id in range(nb_tracks):
    channels=df['tofpet_channel'].iloc[tracks_id[track_id]]
    tofpet=df['tofpet_id'].iloc[tracks_id[track_id]]
    t_stamp=df['timestamp'].iloc[tracks_id[track_id]]*6.25
    t_entry=t_entries[track_id]
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
            delay=electronic_delay_x[pos]

            det_time_x[pos].append(t_ch-dsc_/csc-dcal_/c-t_entry-delay)

    for ind in range(len(index_y)):
        index=index_y[ind]
        dsc_=dsc_y[track_id][ind]
        if not(np.isnan(dsc_)):
            dcal_=dcal_y[track_id][ind]
            chan=channels[index]
            tof_id=tofpet[index]
            t_ch=t_stamp[index]
            pos=ttc.position_in_array(chan,tof_id,'Y')
            delay=electronic_delay_y[pos]
            det_time_y[pos].append(t_ch-dsc_/csc-dcal_/c-t_entry-delay)

meanx=np.zeros(192)
meany=np.zeros(192)


# for i in range (192):
#     plt.figure()
#     plt.hist(det_time_y[i],100)
#     plt.title(str(np.mean(det_time_y[i])))
#     plt.xlabel("Relative residual time")
#     plt.ylabel("Number of events")
#     plt.grid("on")
#     plt.savefig('/home/ecal/Documents/scripts/Analysis/Time_calibration/Graphs/refxchannel'+str(i)+'.png',dpi=300)
#     meany[i]=np.mean(det_time_y[i])

for i in range (192):
    rfa.Gaussian_fit(det_time_y[i],i,'refx62')
    rfa.Gaussian_fit(det_time_y[i],i,'refy62')

#     plt.figure()
#     plt.hist(det_time_x[i],100)
#     plt.title(str(np.mean(det_time_y[i])))
#     plt.xlabel("Relative residual time")
#     plt.ylabel("Number of events")
#     plt.grid("on")
#     plt.savefig('/home/ecal/Documents/scripts/Analysis/Time_calibration/Graphs/refychannel'+str(i)+'.png',dpi=300)
#     meanx[i]=np.mean(det_time_x[i])
# plt.hist(meanx)
# plt.savefig('/home/ecal/Documents/scripts/Analysis/Time_calibration/Graphs/refx.png',dpi=300)
# plt.hist(meany)
# plt.savefig('/home/ecal/Documents/scripts/Analysis/Time_calibration/Graphs/refy.png',dpi=300)
