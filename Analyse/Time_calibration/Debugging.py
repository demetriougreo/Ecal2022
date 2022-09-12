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


## The first part of our debugging structure is to find all the tracks which include the reference point for a given side ##
c=30 ## speed of light
csc=17.526 ## speed of light in the fibre as cm/ns
length=192


df=rfa.merger(['/home/ecal/Documents/scripts/Analysis/Data/10h/data_0000.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0001.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0002.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0003.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0004.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0005.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0006.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0007.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0008.root' ])
tracks=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Track_reconstruction/tracks.csv')## [indexx, indexy, truck-parameter, event_id]
tracks_id=tracks['track_id']
nb_tracks=len(tracks_id)


dsc_y_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dsc_Y.csv')## distance scintillator
dcal_y_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dcal_Y.csv')## Distance travelled between layers 
dsc_x_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dsc_X.csv')
dcal_x_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dcal_X.csv')

dsc_x=[ list(dsc_x_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]
dcal_x=[ list(dcal_x_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]
dsc_y=[ list(dsc_y_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]
dcal_y=[ list(dcal_y_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]

def find_tracks(tofpet_id,channel):## it finds all tracks that happens to pass from a given point 
    counter=0
    for i in range(nb_tracks):
       # print(i)
        #print(tracks['track_id'])
        channels=df['tofpet_channel'].iloc[tracks['track_id'].iloc[i]]
        t_id=df['tofpet_id'].iloc[tracks['track_id'].iloc[i]]
        if any([t_id[i]==tofpet_id and channels[i]==channel for i in range(len(channels))]):
            counter=counter+1
            print('The point has been activated by track '+str(i)+'. The new total is '+str(counter))
    return counter

## that is done in order to find the optimal SiPM to serve as our calibrator ##
# counters=np.zeros(64)
# for i in range(64):
#     counters[i]=find_tracks(0,i)

# print(counters)

## Now we play the game of ice and fire ##
def reference_tracks(ref_id,ref_channel): ## this function extracts only the tracks and corresponding df that pass from the reference point
    data=[]
    track_new=[]
    dsc_x_new=[]
    dsc_y_new=[]
    dcal_x_new=[]
    dcal_y_new=[]
    for track_id in range(nb_tracks):
        channels=df['tofpet_channel'].iloc[tracks_id[track_id]]## we use that because there is no perfect correspondance between the track id and the events as recorded by the tofpet
        tofpet=df['tofpet_id'].iloc[tracks_id[track_id]]## it is convoluted, a perver way to quantify it algorithmically
        if any([tofpet[i]==ref_id and channels[i]==ref_channel for i in range(len(channels))]):
            print(df.iloc[tracks_id[track_id]])
            data.append(df.iloc[tracks_id[track_id]])
            track_new.append(tracks.iloc[track_id])
            dsc_x_new.append(dsc_x[track_id])
            dsc_y_new.append(dsc_y[track_id])
            dcal_x_new.append(dcal_x[track_id])
            dcal_y_new.append(dcal_y[track_id])
    print(data)
    print(track_new)
    df_new=pd.DataFrame(data)
    tr_new=pd.DataFrame(track_new)
    dsc_x_new=pd.DataFrame(dsc_x_new)
    dsc_y_new=pd.DataFrame(dsc_y_new)
    dcal_x_new=pd.DataFrame(dcal_x_new)
    dcal_y_new=pd.DataFrame(dcal_y_new)
    return df_new, tr_new,dsc_x_new,dsc_y_new,dcal_x_new,dcal_y_new## They are created


def reference_time_x(ref_id,ref_channel,tra_id,ind):
    for i in range(len(df['tofpet_id'].iloc[tra_id])):
        if df['tofpet_id'].iloc[tra_id][i]==ref_id & df['tofpet_channel'].iloc[tra_id][i]==ref_channel:
            return df['timestamp'].iloc[tra_id][i]- dsc_x[i][-1]/csc-dcal_x[i][-1]/c## we still need the indices


def reference_time_y(ref_id,ref_channel,tra_id,ind):
    for i in range(len(df['tofpet_id'].iloc[tra_id])):
        if df['tofpet_id'].iloc[tra_id][i]==ref_id & df['tofpet_channel'].iloc[tra_id][i]==ref_channel:
            return df['timestamp'].iloc[tra_id][i]- dsc_y[i][ind]/csc-dcal_y[i][ind]/c## we still need the indices

def find_ref_index(index,channels,tofpet,ref_ch,ref_id):
    for element in index:
        if (channels[element]==ref_ch & tofpet[element]==ref_id):
            return element

def delays(ref_id,ref_channel):
    dt=[[] for i in range(len(df))]
    for track_id in range(len(tracks)):
        channels=df['tofpet_channel'].iloc[track_id]## we use that because there is no perfect correspondance between the track id and the events as recorded by the tofpet
        tofpet=df['tofpet_id'].iloc[track_id]## it is convoluted, a perver way to quantify it algorithmically
        t_stamp=df['timestamp'].iloc[track_id]*6.25
        tr_param=tracks['track_param'].loc[track_id][1:-1].split(',')##break
        tr_param=[float(tr) for tr in tr_param]## convert
        index_y=tracks['index_y'].loc[track_id][1:-1].split(',')
        index_y=[int(y) for y in index_y]
        index_x=tracks['index_x'].loc[track_id][1:-1].split(',')
        index_x=[int(x) for x in index_x]

        if ttc.is_sidex(ref_id):
            hits_other_side=[ttc.Mapping2D(tofpet[i],channels[i]) for i in index_y]  ## we find the position of the hits on the y axis relative to the SiPM under question
        else:
            hits_other_side=[ttc.Mapping2D(tofpet[i],channels[i]) for i in index_x]  ## we find the position of the hits on the x axis relative to the SiPM under question


        suitable, t_entry = ftc.suitable_track([ref_channel,ref_id],channels,tofpet,hits_other_side,t_stamp,tr_param)
        if suitable:
            if ttc.is_sidex(ref_id):
                ind_ref=find_ref_index(index_x,channels,tofpet,ref_id,ref_channel)
                t=reference_time_x(ref_id,ref_channel,ind_ref)
                for ind in index_x:
                     dsc_=dsc_x[track_id][ind]## we have to reconsider
                     if not(np.isnan(dsc_)): ## eliminate the case where there is no side correspondance yet keep the values corresponding to the reference channel 
                        dcal_=dcal_x[track_id][ind]
                        chan=channels[ind]
                        tof_id=tofpet[ind]
                        t_ch=t_stamp[ind]
                        pos=ttc.position_in_array(chan,tof_id,'X')
                        dt[pos].append(t_ch-t-dcal_x/c-dsc_/csc)
            else:
                ind_ref=find_ref_index(index_y,channels,tofpet)
                t=reference_time_y(ref_id,ref_channel,ind_ref)
                for ind in index_x:
                     dsc_=dsc_x[track_id][ind]## we have to reconsider
                     if not(np.isnan(dsc_)): ## eliminate the case where there is no side correspondance yet keep the values corresponding to the reference channel 
                        dcal_=dcal_x[track_id][ind]
                        chan=channels[ind]
                        tof_id=tofpet[ind]
                        t_ch=t_stamp[ind]
                        pos=ttc.position_in_array(chan,tof_id,'X')
                        dt[pos].append(t_ch-t-dcal_x/c-dsc_/csc)

#counter=find_tracks(4,42)
#print(counter)
df_new, tr_new,dsc_x_new,dsc_y_new,dcal_x_new,dcal_y_new=reference_tracks(4,42)
#print(df_new)
#print(tr_new)