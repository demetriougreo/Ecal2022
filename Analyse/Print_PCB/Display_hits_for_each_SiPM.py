#!/usr/bin/env python3

## This scripts prints out the number of hits on the PCB. The noise (1 hit) is not removed from the 
# dataframe df_ecal
import uproot
import uproot3
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt
import mplhep as hep
plt.style.use([hep.style.LHCb])
#%matplotlib inline


nb_files=9

Tname = 'board_57'
channel_events=[[] for i in range(384)]
def arrange (data):
    filepath="/home/ecal/Documents/scripts/Analysis/ECAL_SiPM_mapping.xlsx"
    #print(data)
    position=pd.read_excel(filepath)
    TOFPET=position['TOFPET']
    #Y=position['Layer']         #Looking a the PCB from the side with the SiPM and SiPM subscripts written above
    X=position['Reversed Bar']  #Counting from the left
    Y=position['Reversed Layer'] # Looking at the PCB from behind
    Channel=position['Channel']
    datanew=np.zeros([4,24])
    for i in range(96):
        #print(Y[i])
        datanew[Y[i]-1,X[i]]=data[Channel[i]+32*TOFPET[i]]
    return list(datanew)


# br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel', 'tac', 't_coarse', 't_fine', 'timestamp', 'v_coarse', 'v_fine', 'value', 'timestamp_cal_chi2', 'timestamp_cal_dof', 'value_cal_chi2', 'value_cal_dof', 'value_saturation']
#for root_id in range(nb_files):
root_file =  '/home/ecal/Documents/Data/run_000192/data_0000.root'
br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel']
with uproot.open(root_file) as tree:
    dict_ecal = tree[Tname].arrays(br_list_data, library="np")
df_ecal = pd.DataFrame.from_dict(dict_ecal) 
df_ecal=df_ecal.query('n_hits>5')
# The recorded data is now in this dataframe 

# Let create a list (2D array) recording the events recorded in each SiPM
tofpet_id = df_ecal['tofpet_id'].tolist()
tofpet_channel=df_ecal['tofpet_channel'].tolist() 
nb_events=len(tofpet_channel)
#print(nb_events)
for i in range(nb_events):
    for j in range(len(tofpet_channel[i])):
        ch=tofpet_channel[i][j]
        t_id=tofpet_id[i][j]
        PCB=int(t_id/2)
        if t_id % 2== 0:
            ch=ch+96*PCB
        else:
            ch=ch+96*PCB+32
        channel_events[ch].append(i)

## Print out the number of events for each SiPM of the 4 PCB. Using previous list, the number of events
# is just the length of each array.

PCB1=arrange([len(ch_ev) for ch_ev in channel_events[0:96]])
PCB2=arrange([len(ch_ev) for ch_ev in channel_events[96:192]])
PCB3=arrange([len(ch_ev) for ch_ev in channel_events[192:288]])
PCB4=arrange([len(ch_ev) for ch_ev in channel_events[288:384]])

## Display the PCBs hits and save the image as a .png in the current open folder
plt.matshow(PCB1)
plt.title('Bottom X')
plt.colorbar()
plt.savefig("/home/ecal/Documents/scripts/Analysis/Print_PCB/PCBs/Bottom_X_10.png")
#plt.show()
plt.clf()

plt.matshow(PCB2)
plt.title('Bottom Y')
plt.colorbar()
plt.savefig('/home/ecal/Documents/scripts/Analysis/Print_PCB/PCBs/Bottom_Y_10.png')
#plt.show()
plt.clf()

plt.matshow(PCB3)
plt.title('Top X')
plt.colorbar()
plt.savefig("/home/ecal/Documents/scripts/Analysis/Print_PCB/PCBs/Top_X_10.png")
#plt.show()
plt.clf()

plt.matshow(PCB4)
plt.title('Top Y')
plt.colorbar()
plt.savefig("/home/ecal/Documents/scripts/Analysis/Print_PCB/PCBs/Top_Y_10.png")
#plt.show()
plt.clf()
