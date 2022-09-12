#!/usr/bin/env python3
import uproot
import uproot3
import numpy as np
import pandas as pd
import sys
import track_reconstruction_old as tr


def Create_tracks(Profiling):
    root_file =  '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0000.root'
    Tname = 'board_57'
    br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel', 'tac']#, 't_coarse', 't_fine', 'timestamp', 'v_coarse', 'v_fine', 'value', 'timestamp_cal_chi2', 'timestamp_cal_dof', 'value_cal_chi2', 'value_cal_dof', 'value_saturation']
    
    
    # Extract the data and transform it into a dataframe
    with uproot.open(root_file) as tree:
        dict_ecal = tree[Tname].arrays(br_list_data, library="np")

    df = pd.DataFrame.from_dict(dict_ecal).query('n_hits>6')
    df=df.query('n_hits<18')
    nb_events=100
    steps=9
    matrix=np.empty((nb_events,steps*3))
    matrix[:]=np.NaN
    tracks_to_save=pd.DataFrame(matrix)
    for event_id in range(nb_events):
        channels=df.iloc[event_id]['tofpet_channel']
        tofpet_id=df.iloc[event_id]['tofpet_id']
        layers=tr.same_layer(channels,tofpet_id)# we have now the layers of each hits
        hitsX = []
        hitsY = []
        for hits in range(len(channels)):
            if tr.is_sidex(tofpet_id[hits]):
                hitsX.append(tr.correction2D([channels[hits],tofpet_id[hits],layers[hits]]))
            else:
                hitsY.append(tr.correction2D([channels[hits],tofpet_id[hits],layers[hits]]))

        if len(hitsX)>1 and len(hitsY)>1: ## Some events doesn't have hits on one of the two sides and are thus not considered
            x0,tx,hits_index=tr.tracks(hitsX)
            y0,ty,hits_indey=tr.tracks(hitsY)
        
            z=np.linspace(1,9,steps)
            x=tx*(z-9)+x0
            y=ty*(z-9)+y0
            trackx=[[x[i],z[i]-1] for i in range(steps)]## Track projection on X
            tracky=[[y[i],z[i]-1] for i in range(steps)] ## Track projection on Y
            track=[[x[i],y[i],z[i]-1] for i in range(steps)] ##3D track

            ## Chi_2 test for the tracks determined before
            chix=tr.chi_2(hitsX,trackx,hits_index)
            chiy=tr.chi_2(hitsY,tracky,hits_indey)
    ####                    GRAPHICAL DISPLAY OF THE EVENT              #########
            if chix and chiy:
                tracks_to_save.loc[event_id]=np.array(track).reshape(27)
            else:
                print('A track was not satisfying')
    
    if Profiling:
        return tracks_to_save
    else:
        tracks_to_save.dropna().to_csv('tracks.csv')

Create_tracks(False)