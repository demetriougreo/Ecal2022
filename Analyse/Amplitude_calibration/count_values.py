#!/usr/bin/env python3

# Import the appropriate package
import uproot
import uproot3
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt
import mplhep as hep
plt.style.use([hep.style.LHCb])

ch=57
t_id=4
nb_root=4
values=np.empty([1,1])
for root_id in range(nb_root):
    root_file =  '/home/ecal/Documents/scripts/Analysis/Data/10h/data_000'+str(root_id)+'.root'
    Tname = 'board_57'
    br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel','value','tac']
    with uproot.open(root_file) as tree:
        dict_ecal = tree[Tname].arrays(br_list_data, library="np")
    df_ecal = pd.DataFrame.from_dict(dict_ecal) 
    df_muon=df_ecal.query('n_hits>5')

    tofpet_id = df_muon['tofpet_id'].tolist()
    tofpet_channel=df_muon['tofpet_channel'].tolist()
    value=df_muon['value'].tolist()
    tac=df_muon['tac'].tolist()
    nb_events=len(tofpet_channel)
    for event_id in range(nb_events):
        for i in range(len(tofpet_channel[event_id])):
            channel=tofpet_channel[event_id][i]
            tofp_id=tofpet_id[event_id][i]
            if (channel==ch and tofp_id==t_id):
                values=np.append(values,value[event_id][i])
values=sorted(values)
plt.figure()
plt.hist(values,bins=100)
plt.yscale('log')
plt.show()
