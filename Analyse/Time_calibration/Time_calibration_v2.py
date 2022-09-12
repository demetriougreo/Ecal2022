#!/usr/bin/env python3

## Time calibration of the channels of the PCB
import pandas as pd
import uproot
#import uproot3
import numpy as np
import track_time_calibration as ttc
from matplotlib import pyplot as plt
import Preparation as prep
import statistics as st

c=30 ## speed of light
csc=17.526 ## speed of light in the fibre as cm/ns
max_dt=100  ## adaptive tolerance scheme
tolerence=10**(-4) 

## this region of the code is dedicated to cleaning up the dcal and dsc files to be used later ##
root_file =  '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0002.root'

Tname = 'board_57'
br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel', 'timestamp']#, 't_coarse', 't_fine', 'timestamp', 'v_coarse', 'v_fine', 'value', 'timestamp_cal_chi2', 'timestamp_cal_dof', 'value_cal_chi2', 'value_cal_dof', 'value_saturation']
Side_to_calibrate='all' # choose one the following options, of the surface to be calibrated 'all' 'X' 'Y' #

# Extract the data and transform it into a dataframe
with uproot.open(root_file) as tree:
    dict_ecal = tree[Tname].arrays(br_list_data, library="np")
## REALLY IMPORTANT, THE TIME CALIBRATION MUST BE DONE USIGN THE SAME DATAFRAME AS THE ONE USED TO RECONSTRUCT THE TRACK
df = pd.DataFrame.from_dict(dict_ecal).query('n_hits>6')
df=df.query('n_hits<18')

tracks=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Track_reconstruction/tracks.csv')## [indexx, indexy, truck-parameter, event_id]
tracks_id=tracks['track_id']
nb_tracks=len(tracks_id)


if Side_to_calibrate=='all': ## number of channels 
    length=384
else:
    length=192

prep.Preparation('X',root_file)
prep.Preparation('Y',root_file)

dsc_y_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dsc_Y.csv')
dcal_y_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dcal_Y.csv')
dsc_x_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dsc_X.csv')
dcal_x_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dcal_X.csv')

dsc_x=[ list(dsc_x_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]
dcal_x=[ list(dcal_x_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]
dsc_y=[ list(dsc_y_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]
dcal_y=[ list(dcal_y_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]


electronic_delay=np.zeros(length)
dt=[[] for i in range(length)] ## electronic delay for each channel

for track_id in range(length):
    index_x=tracks['index_x'].loc[track_id][1:-1].split(',')
    index_x=[int(x) for x in index_x]

    channels=df['tofpet_channel'].iloc[tracks_id[track_id]]
    tofpet=df['tofpet_id'].iloc[tracks_id[track_id]]
    tstamp=df['timestamp'].iloc[tracks_id[track_id]]

    for ind in range(len(index_x)):
        index=index_x[ind]
        dsc_=dsc_x[track_id][ind]

        if not(np.isnan(dsc_)): ## eliminate the case where there is no side correspondance
            dcal_=dcal_x[track_id][ind]
            ch=channels[index]
            t_id=tofpet[index]
            t_stamp=tstamp[index]
            pos=ttc.position_in_array(ch,t_id,'X')
            t=dsc_/csc+dcal_/c-np.mean([electronic_delay[ttc.position_in_array(channels[index1],tofpet[index1],'X')] for index1 in index_x])
            dt[pos].append(t_stamp-t)

    index_y=tracks['index_y'].loc[track_id][1:-1].split(',')
    index_y=[int(y) for y in index_y]

    channels=df['tofpet_channel'].iloc[tracks_id[track_id]]
    tofpet=df['tofpet_id'].iloc[tracks_id[track_id]]
    tstamp=df['timestamp'].iloc[tracks_id[track_id]]

    for ind in range(len(index_y)):
        index=index_y[ind]
        dsc_=dsc_y[track_id][ind]

        if not(np.isnan(dsc_)): ## eliminate the case where there is no side correspondance
            dcal_=dcal_y[track_id][ind]
            ch=channels[index]
            t_id=tofpet[index]
            t_stamp=tstamp[index]
            pos=ttc.position_in_array(ch,t_id,'Y')
            t=dsc_/csc+dcal_/c
            dt[pos].append(t_stamp-t)   
pd.DataFrame(dt).to_csv('Electronic_delay_5.csv')   
