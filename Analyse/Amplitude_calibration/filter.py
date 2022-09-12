#!/usr/bin/env python3

# Functions used to filter the hits of an event that can be associated to noise, each channel and 
# tac have it own offset and distribution for muon events, the idea is to remove the offset 
# for each hit of the event and then verifies that the value lies inside a range of 2sigmas around 
# the mean value of a muon event. As said before all of the offset, mean and standard deviation
#will depend on the channel and the tac
# 100 events~1s
import time 
import uproot
import uproot3
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt
import mplhep as hep
plt.style.use([hep.style.LHCb])
#%matplotlib inline
import warnings
warnings.filterwarnings("ignore")

def in_range(value,noise,qdc,sqdc):
    if abs(value-noise-qdc)<sqdc:
        return True
    else:
        return False


def filter(event):
    noise=pd.read_csv('noise.csv')
    QDC=pd.read_csv('QDC.csv')
    tofpet_id = event['tofpet_id']
    tofpet_channel=event['tofpet_channel']
    value=event['value']
    tac=event['tac']
    to_remove=[]
    for hit in range(len(tofpet_channel)):
        t_id=tofpet_id[hit]
        PCB=int(t_id/2)
        if t_id % 2== 0:
            ch=tofpet_channel[hit]+96*PCB
        else:
            ch=tofpet_channel[hit]+96*PCB+32
        tacstr='tac'+str(tac[hit])
        sigmastr='sigma'+str(tac[hit])
        noise_,qdc,sqdc=noise[tacstr][ch],QDC[tacstr][ch],QDC[sigmastr][ch]
        if not(in_range(value[hit],noise_,qdc,sqdc)):
            to_remove.append(hit)
    event['tofpet_id']=np.delete(event['tofpet_id'],to_remove)
    event['tofpet_channel']=np.delete(event['tofpet_channel'],to_remove)
    event['tac']=np.delete(event['tac'],to_remove)
    event['value']=np.delete(event['value'],to_remove)
    event_filtred=event
    return event_filtred



root_file =  '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0000.root'
Tname = 'board_57'
# br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel', 'tac', 't_coarse', 't_fine', 'timestamp', 'v_coarse', 'v_fine', 'value', 'timestamp_cal_chi2', 'timestamp_cal_dof', 'value_cal_chi2', 'value_cal_dof', 'value_saturation']
br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel','tac','value']
with uproot.open(root_file) as tree:
    dict_ecal = tree[Tname].arrays(br_list_data, library="np")
df_ecal = pd.DataFrame.from_dict(dict_ecal) 
df_ecal_TBF=df_ecal.query('n_hits>5')# look only for event that could be muons TBF holds to To Be Filtred
# The recorded data is now in this dataframe 
nb_events=len(df_ecal_TBF.index)
print(nb_events)
t0=time.time()
for i  in range(200):
    event_TBF=df_ecal_TBF.iloc[i]
    event=filter(event_TBF)
dt=time.time()-t0
print(dt)
