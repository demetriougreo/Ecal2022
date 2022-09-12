#!/usr/bin/env python3

## Time calibration of the channels of the PCB
import pandas as pd
import uproot
import uproot3
import numpy as np
import track_time_calibration as ttc
import Preparation as prep
import statistics as st

c=30 ## speed of light
csc=17.526 ## speed of light in the fibre as cm/ns
conv_param=1  ## adaptive tolerance scheme
tolerence=10**(-4) 

root_file =  '/home/ecal/Documents/Data/run_000192/data_0000.root'
Tname = 'board_57'
br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel', 'timestamp']#, 't_coarse', 't_fine', 'timestamp', 'v_coarse', 'v_fine', 'value', 'timestamp_cal_chi2', 'timestamp_cal_dof', 'value_cal_chi2', 'value_cal_dof', 'value_saturation']

# Extract the data and transform it into a dataframe
with uproot.open(root_file) as tree:
    dict_ecal = tree[Tname].arrays(br_list_data, library="np")

## REALLY IMPORTANT, THE TIME CALIBRATION MUST BE DONE USIGN THE SAME DATAFRAME AS THE ONE USED TO RECONSTRUCT THE TRACK
df = pd.DataFrame.from_dict(dict_ecal).query('n_hits>6')
df=df.query('n_hits<18')

tracks=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Track_reconstruction/tracks.csv')## [indexx, indexy, truck-parameter, event_id]
tracks_id=tracks['track_id']
nb_tracks=len(tracks_id)

length=384
print('Preparation started')
dsc_x,dcal_x,t_entry_x=prep.Preparation('X',root_file)
dsc_y,dcal_y,t_entry_y=prep.Preparation('Y',root_file)
print('Preparation finished')

electronic_delay=np.zeros(length)
while conv_param>tolerence:
    dt=[[] for i in range(length)] ## electronic delay for each channel
    for track_id in range(2000):
        
        channels=df['tofpet_channel'].iloc[tracks_id[track_id]]
        tofpet=df['tofpet_id'].iloc[tracks_id[track_id]]
        tstamp=df['timestamp'].iloc[tracks_id[track_id]]*6.25

        index_x=tracks['index_x'].loc[track_id][1:-1].split(',')
        index_x=[int(x) for x in index_x]
        t_x=t_entry_x[track_id]
        for ind in range(len(index_x)):
            index=index_x[ind]
            dsc_=dsc_x[track_id][ind]

            if not(np.isnan(dsc_)): ## eliminate the case where there is no side correspondance
                dcal_=dcal_x[track_id][ind]
                ch=channels[index]
                t_id=tofpet[index]
                t_stamp=tstamp[index]*6.25
                pos=ttc.position_in_array(ch,t_id)
                t=t_x+dsc_/csc+dcal_/c-st.mean([electronic_delay[ttc.position_in_array(channels[index1],tofpet[index1])] for index1 in index_x])
                dt[pos].append(t_stamp-t)

        index_y=tracks['index_y'].loc[track_id][1:-1].split(',')
        index_y=[int(y) for y in index_y]      
        t_y=t_entry_y[track_id]

        for ind in range(len(index_y)):
            index=index_y[ind]
            dsc_=dsc_y[track_id][ind]

            if not(np.isnan(dsc_)): ## eliminate the case where there is no side correspondance
                dcal_=dcal_y[track_id][ind]
                ch=channels[index]
                t_id=tofpet[index]
                t_stamp=tstamp[index]*6.25
                pos=ttc.position_in_array(ch,t_id)
                t=t_y+dsc_/csc+dcal_/c-st.mean([electronic_delay[ttc.position_in_array(channels[index1],tofpet[index1])] for index1 in index_y])
                dt[pos].append(t_stamp-t)

    conv_param=max([abs(st.mean(dt[k])-electronic_delay[k]) for k in range(length)])
    electronic_delay=[st.mean(dt[k]) for k in range(length)]
    print(electronic_delay)

pd.DataFrame(electronic_delay).to_csv('Electronic_delay_new.csv')  
