# Contain main function used for time calibration

from operator import index
import numpy as np
import pandas as pd
import math as mt
import track_time_calibration as ttc

def suitable_track (ref,channels,tofpets,hits_other_side,t_stamp,track_param):
    c=30 #cm/ns
    csc=17.526
    ch=ref[0]
    t_id=ref[1]
    if ttc.is_sidex(t_id):
        side='X'
    else:
        side='Y'
    coor_ref=ttc.Mapping2D(t_id,ch)## find the coordinates of the reference channel
    events_with_ref=[] ## events which can be referenced to the reference channel
    if any([tofpets[i]==t_id and channels[i]==ch for i in range(len(channels))]):## if we can referecne this track to the channel under question
        dsc_=ttc.dsc(hits_other_side,coor_ref[1]) ## we have to test it. It is potentially erroneous
        if not( np.isnan(dsc_)):
            t_stamp_ref=t_stamp[np.argwhere([tofpets[i]==t_id and channels[i]==ch for i in range(len(channels))])][0][0]# we find the average timestamp of the ref_point
            dcal_=ttc.dcal(track_param,coor_ref,dsc_,side)## that corresponds to the dcal of the reference point
            t_entry=t_stamp_ref-dsc_/csc-dcal_/c## so this is equal to t_entry of the reference point. Here the system gets 
            ## a bit convoluted because this quantity would later be used for the relative delay calculation
            return True , t_entry
    return False,0

def find_new_ref(channels,t_id,previous_ref):
    ## Step 1: Map the previous reference point into the geometry of the hardware
    coor_prev_ref=ttc.Mapping2D(previous_ref[1],previous_ref[0])
    ## Step 2:: Find the distances between the previous refernce point and the potential reference points
    distances=[np.sqrt((coor_prev_ref[0]-ttc.Mapping2D(t_id[i],channels[i])[0])**2+(coor_prev_ref[1]-ttc.Mapping2D(t_id[i],channels[i])[1])**2) for i in range(len(channels))]
    ## This is a questionable choice, but I can see where it might come from. We take the potential reference point which is located the furthest possible from the 
    ## existing reference point. The equation above by the way is wrong. Cn you spot the mistake :) ?? 
    index_max=distances.index(max(distances))
    return channels[index_max],t_id[index_max]

def to_ch_t_id (pos_in_array,already_used,side):
    pos_in_array=[pos for pos in pos_in_array if not(pos in already_used)]

    if side=='X':
        t_id=[4*mt.trunc(pos/96.0)+mt.trunc((pos%96)/64.0) for pos in pos_in_array]
    if side=='Y':
        t_id=[4*mt.trunc(pos/96.0)+mt.trunc((pos%96)/64.0)+2 for pos in pos_in_array]

    channels=[pos_in_array[i]%96-32 if t_id[i]%2==1 else pos_in_array[i]%96 for i in range(len(t_id))]
    return channels,t_id

