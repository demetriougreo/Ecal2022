#!/usr/bin/env python3

# Import the appropriate package
import uproot
#import uproot3
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt
#import mplhep as hep
#plt.style.use([hep.style.LHCb])


interm_df=pd.DataFrame([[[],[],[],[]] for i in range(384)],columns=['tac0','tac1','tac2','tac3'])
interm1_df=pd.DataFrame([[[],[],[],[]] for i in range(384)],columns=['tac0','tac1','tac2','tac3'])
nb_root=1
for root_id in range(nb_root):
    root_file =  '/home/ecal/Documents/Data/run_000204/data_000'+str(root_id)+'.root'
    Tname = 'board_57'
    br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel','value','tac']
    with uproot.open(root_file) as tree:
        dict_ecal = tree[Tname].arrays(br_list_data, library="np")
    df_ecal = pd.DataFrame.from_dict(dict_ecal) 
    ## Extract the data into a Dataframe

    # Select the number of hits we want: n_hits==1 is noise and n_hits>5 are muons events
    df_noise=df_ecal.query('n_hits==1')
    df_muon=df_ecal.query('n_hits>5')
    df_muon=df_ecal.query('n_hits<15')

    tofpet_id = df_noise['tofpet_id'].tolist()
    tofpet_channel=df_noise['tofpet_channel'].tolist()
    value=df_noise['value'].tolist()
    tac=df_noise['tac'].tolist()
    nb_events=len(tofpet_channel)
    print(nb_events)
    for event_id in range(nb_events):
        for i in range(len(tofpet_channel[event_id])):
            tacstr='tac'+str(tac[event_id][i])
            ch=tofpet_channel[event_id][i]
            t_id=tofpet_id[event_id][i]
            PCB=int(t_id/2)
            if t_id % 2== 0:
                ch=ch+96*PCB
            else:
                ch=ch+96*PCB+32
            interm_df[tacstr][ch].append(value[event_id][i])

    ## Do the same as before but using data comming from muon events
    tofpet_id = df_muon['tofpet_id'].tolist()
    tofpet_channel=df_muon['tofpet_channel'].tolist()
    value=df_muon['value'].tolist()
    tac=df_muon['tac'].tolist()
    nb_events=len(tofpet_channel)
    for event_id in range(nb_events):
        
        for i in range(len(tofpet_channel[event_id])):
            tacstr='tac'+str(tac[event_id][i])
            ch=tofpet_channel[event_id][i]
            t_id=tofpet_id[event_id][i]
            PCB=int(t_id/2)
            if t_id % 2== 0:
                ch=ch+96*PCB
            else:
                ch=ch+96*PCB+32
            interm1_df[tacstr][ch].append(value[event_id][i])
    
print(interm_df['tac0'].iloc[220])
noise_channel=pd.DataFrame([[np.mean(interm_df['tac0'].iloc[ch]),np.mean(interm_df['tac1'].iloc[ch]),np.mean(interm_df['tac2'].iloc[ch]),np.mean(interm_df['tac3'].iloc[ch]),np.std(interm_df['tac0'].iloc[ch]),np.std(interm_df['tac1'].iloc[ch]),np.std(interm_df['tac2'].iloc[ch]),np.std(interm_df['tac3'].iloc[ch])] for ch in range(384)], columns=['tac0','tac1','tac2','tac3','sigma0','sigma1','sigma2','sigma3'])
noise_channel.to_csv('noise3.csv')

df_muon=pd.DataFrame([[np.mean(interm1_df['tac0'].iloc[ch]),np.mean(interm1_df['tac1'].iloc[ch]),np.mean(interm1_df['tac2'].iloc[ch]),np.mean(interm1_df['tac3'].iloc[ch]),np.std(interm_df['tac0'].iloc[ch]),np.std(interm_df['tac1'].iloc[ch]),np.std(interm_df['tac2'].iloc[ch]),np.std(interm_df['tac3'].iloc[ch])] for ch in range(384)], columns=['tac0','tac1','tac2','tac3','sigma0','sigma1','sigma2','sigma3'])
df_muon.to_csv('muon3.csv')

df_QDC=df_muon.subtract(noise_channel)
#Replace standard dev by the muon std
for i in range(4):
    sigma='sigma'+str(i)
    df_QDC[sigma]=df_muon[sigma]
df_QDC.to_csv('QDC3.csv')

