#!/usr/bin/env python3

## 
from cmath import isnan
import pandas as pd
import uproot
import uproot3
import numpy as np
import track_time_calibration as ttc
import warnings
warnings.filterwarnings("ignore") 

def Preparation (side,root_file):

    df=root_file
    tracks=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Track_reconstruction/tracks.csv')
    tracks_id=tracks['track_id']
    nb_tracks=len(tracks_id)


    dsc=[[] for i in range(nb_tracks) ]
    dcal=[[] for i in range(nb_tracks)]
    t_entry=list(np.zeros(nb_tracks))

    for track_id in range(nb_tracks):
        print(track_id)
        index_x=tracks['index_x'].loc[track_id][1:-1].split(',')
        index_x=[int(x) for x in index_x]
        print(index_x)
        index_y=tracks['index_y'].loc[track_id][1:-1].split(',')
        index_y=[int(y) for y in index_y]
        print(index_y)
        tr_param=tracks['track_param'].loc[track_id][1:-1].split(',')
        tr_param=[float(tr) for tr in tr_param]
        channels=df['tofpet_channel'].iloc[tracks_id[track_id]]## it is a bit convoluted but okay. It simply goes into tracks['track_id'] and get the actual id of the track, because we skip a bit if the track is not sufficiently reconstructed
        tofpet=df['tofpet_id'].iloc[tracks_id[track_id]]## the same as before
        tstamp=df['timestamp'].iloc[tracks_id[track_id]]*6.25
        hits_side_X=[ttc.Mapping2D(tofpet[i],channels[i]) for i in index_x]
        hits_side_Y=[ttc.Mapping2D(tofpet[i],channels[i]) for i in index_y]        
        if side=='X':
            dsc[track_id]=[ ttc.dsc(hits_side_Y,ttc.Mapping2D(tofpet[index_],channels[index_])[1]) for index_ in index_x]
            dcal[track_id]=[ttc.dcal(tr_param,ttc.Mapping2D(tofpet[index_x[i]],channels[index_x[i]]),dsc[track_id][i],'X') for i in range(len(index_x))]
        if side=='Y':
            dsc[track_id]=[ ttc.dsc(hits_side_X,ttc.Mapping2D(tofpet[index_],channels[index_])[1]) for index_ in index_y]
            #print(dsc[track_id])
            dcal[track_id]=[ttc.dcal(tr_param,ttc.Mapping2D(tofpet[index_y[i]],channels[index_y[i]]),dsc[track_id][i],'Y') for i in range(len(index_y))]
        print("out")
    #print(dcal)
    name1='dsc_'+side+'.csv'    
    name2='dcal_'+side+'.csv'
    print("Just before")
    pd.DataFrame(dsc).to_csv(name1)
    print("Just After")
    pd.DataFrame(dcal).to_csv(name2)
    print("The end")



