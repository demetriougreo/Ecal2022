#!/usr/bin/env python3
import uproot
#import uproot3
import numpy as np
import pandas as pd
#import sys
import track_reconstruction as tr
import sys
sys.path.insert(1, '/home/ecal/Documents/scripts/Analysis/Time_calibration')
import Root_files_addition as rfa



def Create_tracks(Profiling):
    tracks_to_save=pd.DataFrame(columns=['index_x','index_y','track_param','track_id'])
    df=rfa.merger(['/home/ecal/Documents/scripts/Analysis/Data/10h/data_0000.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0001.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0002.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0003.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0004.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0005.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0006.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0007.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0008.root' ])
    nb_events=len(df['n_hits'])
    steps=9
    for event_id in range(nb_events):
        print('Event number: '+str(event_id)+' over '+str(nb_events))
        channels=df.iloc[event_id]['tofpet_channel']
        tofpet_id=df.iloc[event_id]['tofpet_id']
        print(tofpet_id)
        hitsX=[tr.Mapping2D(tofpet_id[hits],channels[hits]) for hits in range(len(channels)) if tr.is_sidex(tofpet_id[hits])]
        hitsY=[tr.Mapping2D(tofpet_id[hits],channels[hits]) for hits in range(len(channels)) if not(tr.is_sidex(tofpet_id[hits]))]
        index_x=[hits for hits in range(len(channels)) if tr.is_sidex(tofpet_id[hits])] # index we need for the time calibration
        index_y=[hits for hits in range(len(channels)) if not(tr.is_sidex(tofpet_id[hits]))]# index we need for the time calibration
        if len(hitsX)>1 and len(hitsY)>1: ## Some events doesn't have hits on one of the two sides and are thus not considered
            x0,tx,hits_index=tr.tracks(hitsX)
            y0,ty,hits_indey=tr.tracks(hitsY)
            steps=9
            z=np.linspace(1,9,steps)
            x=tx*(z-9)*2+x0
            y=ty*(z-9)*2+y0
            trackx=[[x[i],(z[i]-1)*2] for i in range(steps)]## Track projection on X
            tracky=[[y[i],(z[i]-1)*2] for i in range(steps)] ## Track projection on Y

            ## Chi_2 test for the tracks determined before
            chix=tr.chi_2(hitsX,trackx,hits_index)
            chiy=tr.chi_2(hitsY,tracky,hits_indey)

    ####            Saving the tracks in a .csv file   #####
            if chix and chiy:
                tracks_to_save=tracks_to_save.append(dict(zip(tracks_to_save.columns,[index_x,index_y,[x0,tx,y0,ty],event_id])),ignore_index=True)
            else:
                print('A track was not satisfying')
    
    if Profiling:
        return tracks_to_save
    else:
        tracks_to_save.to_csv('tracks.csv')

Create_tracks(False)