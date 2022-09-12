# Contain main function used for time calibration

import numpy as np
import pandas as pd
import math as mt

def entering_from_above(x,y):
    if 0<=x<=24 and 0<=y<=24:
        return True
    else:
        return False

# Hits contains the coordinates of the SiPMs that received light and that are on the other side of the calorimeter and 
# belong to the reconstructed track, layer is the layer of the the channel that we are calibrating
def dsc(hits,layer):
    z=[hit[1] for hit in hits]
    matching_layer=[i for i in range(len(z)) if z[i]==layer]
    if len(matching_layer)==0:
        return np.nan
    else:
        return 1.6*np.mean([hits[good_index][0] for good_index in matching_layer])

def dsc_residue():
    return

def dcal(track_param,hit_coor,dsc,side):
    x0=track_param[0]
    y0=track_param[2]
    if side=='X':
        coor=[hit_coor[0]*1.6,dsc,hit_coor[1]*2.0]
    else:
        coor=[dsc,hit_coor[0]*1.6,hit_coor[1]*2.0]
     
    if entering_from_above(x0/1.6,y0/1.6):
        dcal=np.sqrt((coor[0]-x0)**2+(coor[1]-y0)**2+(coor[2]-18)**2)## potentially wrong 
    else:
        tx=track_param[1]
        ty=track_param[3]
        if  x0<0:
            if tx<10**(-3):
                z0=18
            else:    
                z0=x0/tx+18
            x0=0
            y0=y0-ty*(z0-18)
        elif x0/1.6>24:
            if tx<10**(-3):
                z0=18
            else:
                z0=(x0-24*1.6)/tx+18
            x0=24*1.6  
            y0=y0-ty*(z0-18)
        elif  y0<0:
            if ty<10**(-3):
                z0=18
            else:
                z0=y0/ty+18
            y0=0
            x0=x0-tx*(z0-18)

        elif y0/1.6>24:
            if ty<10**(-3):
                z0=18
            else:
                z0=(y0-24*1.6)/ty+18
            y0=24  
            x0=x0-tx*(x0-18)  
         
        dcal=np.sqrt((coor[0]-x0)**2+(coor[1]-y0)**2+(coor[2]-z0)**2)

    return dcal


def dcal_residue():
    return
    
# Ch is the the index of the channel that we are calibrating, hits are the hits observed on the side of ch, exculing this channel
# t_stamp is the time stamp of those channels
def determine_t_entry(hits,hits_other_side,t_stamp,track_param,side):
    c=30            
    csc=17.526  #cm/ns
    nb_hits=len(hits)
    t_entry=np.mean([t_stamp[hit_id]-dcal(track_param,hits[hit_id],dsc(hits_other_side,hits[hit_id][1]),side)/c-dsc(hits_other_side,hits[hit_id][1])/csc for hit_id in range(nb_hits) if not(mt.isnan(dsc(hits_other_side,hits[hit_id][1] ) ) ) ] )
    return t_entry

def position_in_array(channel,t_id,side='all'):
    if side=='all':
        return channel+int(t_id/2)*96+32*np.mod(t_id,2)
    else:
        if is_sidex(t_id):
            return channel+32*np.mod(t_id,2) + 96*int(t_id/4)
        else:
            t_id=t_id-2
            return channel+32*np.mod(t_id,2) + 96*int(t_id/4)

### Functions copied form track_reconstruction.py 


# Determine the (X,Z) or (Y,Z) coordinate of a hits, depending on what tofpet_id is entered. Triplet=[channel,t_id,layer]
def Mapping2D(t_id,channel):
    mapping=[[  [10 , 3], [22 , 3], [ 3 , 3], [15 , 3], [ 9 , 3], [21 , 3], [ 4 , 3], [16 , 3], [ 8 , 3], [20 , 3], [ 5 , 3], [17 , 3], [ 7 , 3], [19 , 3], [ 6 , 3], [18 , 3], [ 7 , 2], [24 , 2], [ 1 , 2], [13 , 2], [ 8 , 2], [23 , 2], [ 2 , 2], [14 , 2], [ 9 , 2], [22 , 2], [ 3 , 2], [15 , 2], [10 , 2], [21 , 2], [ 4 , 2], [16 , 2], [11 , 2], [20 , 2], [ 5 , 2], [17 , 2], [12 , 2], [19 , 2], [ 6 , 2], [18  ,2], [ 7 , 1], [24 , 1], [ 1 , 1], [13 , 1], [ 8 , 1], [23 , 1], [ 2 , 1], [14 , 1], [ 9 , 1], [22 , 1], [ 3 , 1], [15 , 1], [10 , 1], [21 , 1], [ 4 , 1], [16 , 1], [11  ,1], [20 , 1], [ 5 , 1], [17 , 1], [12 , 1], [19 , 1], [ 6 , 1], [18 , 1],[ 7,  4], [24,  4], [ 1,  4], [13,  4], [ 8,  4], [23,  4], [ 2,  4], [14,  4], [ 9,  4], [22,  4], [ 3,  4], [15,  4], [10,  4], [21,  4], [ 4,  4], [16,  4], [11,  4], [20,  4], [ 5,  4], [17,  4], [12,  4], [19,  4], [ 6,  4], [18,  4], [12,  3], [24,  3], [ 1,  3], [13,  3], [11,  3], [23,  3], [ 2,  3], [14,  3]],[[10,  7], [22,  7], [ 3,  7], [15,  7], [ 9,  7], [21,  7], [ 4,  7], [16,  7], [ 8,  7], [20,  7], [ 5,  7], [17,  7], [ 7,  7], [19,  7], [ 6,  7], [18,  7], [ 7,  6], [24,  6], [ 1,  6], [13,  6], [ 8,  6], [23,  6], [ 2,  6], [14,  6], [ 9,  6], [22,  6], [ 3,  6], [15,  6], [10 , 6], [21,  6], [ 4,  6], [16,  6], [11,  6], [20,  6], [ 5,  6], [17,  6], [12,  6], [19,  6], [ 6,  6], [18,  6], [ 7,  5], [24,  5], [ 1,  5], [13,  5], [ 8,  5], [23,  5], [ 2,  5], [14,  5], [ 9,  5], [22,  5], [ 3,  5], [15,  5], [10,  5], [21,  5], [ 4,  5], [16 , 5], [11,  5], [20,  5], [ 5,  5], [17,  5], [12,  5], [19,  5], [ 6,  5], [18,  5],[ 7 , 8], [24 , 8], [ 1 , 8], [13 , 8], [ 8 , 8], [23 , 8], [ 2 , 8], [14 , 8], [ 9 , 8], [22 , 8], [ 3 , 8], [15 , 8], [10,  8], [21 , 8], [ 4 , 8], [16 , 8], [11 , 8], [20 , 8], [ 5 , 8], [17 , 8], [12 , 8], [19 , 8], [ 6 , 8], [18 , 8], [12 , 7], [24 , 7], [ 1 , 7], [13 , 7], [11 , 7], [23 , 7], [ 2 , 7], [14 , 7]]] ##
    if is_sidex(t_id):
        return mapping[int(t_id/4)][channel+32*np.mod(t_id,2)]
    else:
        t_id=t_id-2
        return mapping[int(t_id/4)][channel+32*np.mod(t_id,2)]    

def is_sidex(a):
    if(a==0 or a==1 or a==4 or a==5):
        return 1
    else:
        return 0


