#!/usr/bin/env python3
from datetime import datetime
import stat
import uproot
import uproot3
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt
import mplhep as hep
from itertools import combinations
from vpython import *
from time import *
import turtle
from mpl_toolkits.mplot3d import Axes3D
plt.style.use([hep.style.LHCb])
import track_reconstruction as tr

## This code determine muon tracks using Hough transform on the hits projected on each side of the ECAL.
## This code works for events with only one track.


root_file =  '/home/ecal/Documents/Data/run_000203/data_0000.root'
#root_file =  '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0000.root'

Tname = 'board_57'
br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel', 'tac','value']#, 't_coarse', 't_fine', 'timestamp', 'v_coarse', 'v_fine', 'value', 'timestamp_cal_chi2', 'timestamp_cal_dof', 'value_cal_chi2', 'value_cal_dof', 'value_saturation']

running=1
#####   FUNCTION FOR GRAPHICAL DISPLAY OF THE TRACK AND THE HITS PROJECTED ON EACH SIDE #######

# Extract the data and transform it into a dataframe
with uproot.open(root_file) as tree:
    dict_ecal = tree[Tname].arrays(br_list_data, library="np")

df = pd.DataFrame.from_dict(dict_ecal)
df['color'] = df['value']
df['color'] = df.loc[:, 'value']
df['id'] = range(1, len(df) + 1)
min_=np.min([np.min(col) for col in df['color']])
max_=np.max([np.max(col) for col in df['color']])
#we renormalize
df['color']=(df['color']+abs(min_))
df['color']=df['color']/(abs(max_)+abs(min_))

#df_events_tmp=[]
#for i in range(len(df)):
#    if df.iloc[i]['n_hits']>32:
#        df_events_tmp.append(df_events.iloc[i])
#df_events = pd.DataFrame(df_events_tmp)
#df = df.loc[df['n_hits'] > 32]
#print(df['color'])
df = df.loc[df['n_hits'] < 20]
df = df.loc[df['n_hits'] > 6]

def Run(b):
    global running
    if running==True:
        b.text="Run"
        running=0
    else:
        b.text="Pause"
        running=1



c1 = canvas(background=color.black, width=2000, height=600)
c1.camera.pos = vector(30,8,0)
c2 = canvas(background=color.black, width=2000, height=600)
c2.camera.pos = vector(30,8,0)
for i in range(100):
    box(canvas=c1, pos=vector(1.6*30, 2*(0.5+i*0.08)-1, 0), color=vector(1,1-float(i/100),0), length=1.6*2, width=2*0.1, height=1.6*0.08)

text(canvas=c1, text=str(min_), pos=vector(1.6*34, 2*0.5-1, 0), height=2*0.5, depth=0.01, color=color.white, axis=vector(1, 0, 0))
text(canvas=c1, text=str(max_-(max_-min_)/4), pos=vector(1.6*34, 2*6.5-1, 0),  height=2*0.5, depth=0.01, color=color.white, axis=vector(1, 0, 0))
text(canvas=c1, text=str(max_-(max_-min_)/2), pos=vector(1.6*34, 2*4.5-1, 0), height=2*0.5, depth=0.01, color=color.white, axis=vector(1, 0, 0))
text(canvas=c1, text=str(max_-(max_-min_)/4*3), pos=vector(1.6*34, 2*2.5-1, 0), height=2*0.5, depth=0.01, color=color.white, axis=vector(1, 0, 0))
text(canvas=c1, text=str(max_), pos=vector(1.6*34, 2*8.5-1, 0), height=2*0.5, depth=0.01, color=color.white, axis=vector(1, 0, 0))


for i in range(100):
    box(canvas=c2, pos=vector(1.6*30, 2*(0.5+i*0.08)-1, 0), color=vector(1,1-float(i/100),0), length=1.6*2, width=2*0.1, height=1.6*0.08)

text(canvas=c2, text=str(min_), pos=vector(1.6*34, 2*0.5-1, 0), height=2*0.5, depth=0.01, color=color.white, axis=vector(1, 0, 0))
text(canvas=c2, text=str(max_-(max_-min_)/4), pos=vector(1.6*34, 2*6.5-1, 0),  height=2*0.5, depth=0.01, color=color.white, axis=vector(1, 0, 0))
text(canvas=c2, text=str(max_-(max_-min_)/2), pos=vector(1.6*34, 2*4.5-1, 0), height=2*0.5, depth=0.01, color=color.white, axis=vector(1, 0, 0))
text(canvas=c2, text=str(max_-(max_-min_)/4*3), pos=vector(1.6*34, 2*2.5-1, 0), height=2*0.5, depth=0.01, color=color.white, axis=vector(1, 0, 0))
text(canvas=c2, text=str(max_), pos=vector(1.6*34, 2*8.5-1, 0), height=2*0.5, depth=0.01, color=color.white, axis=vector(1, 0, 0))


cubex_dictionary = {}
for i in range(1, 25):
    for j in range(1, 9):
        cubex_dictionary["mybox1" + str(i) + str(j)] = box(canvas=c1, pos=vector(1.6*i+0.8, 2*j-1, 0), length=1.6*0.8, height=2*0.8,width=0.01, color=color.white, shininess=False)
#        distant_light(direction=vector(i, j, 0), color=color.white)
distant_light(canvas=c1, direction=vector(0, 0, 0), color=color.white)
distant_light(canvas=c1, direction=vector(39, 18, 0), color=color.white)

cubey_dictionary = {}
for i in range(1, 25):
    for j in range(1, 9):
        cubey_dictionary["mybox2" + str(i) + str(j)] = box(canvas=c2, pos=vector(1.6*i+0.8, 2*j-1, 0), length=1.6*0.8, height=2*0.8,width=0.01, color=color.white, shininess=False)
        #distant_light(direction=vector(i, j, 0), color=color.white)
distant_light(canvas=c2, direction=vector(0, 0, 0), color=color.white)
distant_light(canvas=c2, direction=vector(39, 18, 0), color=color.white)


def Visual_Presentation(data1, data2,trackx,tracky,colorx,colory):
    samples=100
    events_dictionary={}
    for i in range(len(data1)):
        cubex_dictionary["mybox1" + str(data1[i][0]) + str(data1[i][1])].color=vector(1, colorx[i], 0)
    events_dictionary["curvedx"]=curve(canvas=c1,pos=[vector(trackx[0][0],trackx[0][1],0.4),vector(trackx[-1][0],trackx[-1][1],0)],radius=0.2,color=color.yellow)
    events_dictionary["curvedy"]=curve(canvas=c2,pos=[vector(tracky[0][0],tracky[0][1],0.4),vector(tracky[-1][0],tracky[-1][1],0)],radius=0.2,color=color.yellow)
    for i in range(len(data2)):
            cubey_dictionary["mybox2" + str(data2[i][0]) + str(data2[i][1])].color=vector(1, colory[i], 0)
    temp=0
    while temp < samples:
        rate(50)
        if (running == 1):
            temp = temp + 1
        pass
    for i in range(len(data1)):
        cubex_dictionary["mybox1" + str(data1[i][0]) + str(data1[i][1])].color = color.white
    for i in range(len(data2)):
        cubey_dictionary["mybox2" + str(data2[i][0]) + str(data2[i][1])].color = color.white
    events_dictionary["curvedx"].visible=False
    events_dictionary["curvedx"].delete()
    events_dictionary["curvedy"].visible=False
    events_dictionary["curvedy"].delete()
                                ##############

button(text="Pause",pos=c1.title_anchor,bind=Run)


for event_id in range(len(df)):
    channels=df.iloc[event_id]['tofpet_channel']
    tofpet_id=df.iloc[event_id]['tofpet_id']
    hitsX=[tr.Mapping2D(tofpet_id[hits],channels[hits]) for hits in range(len(channels)) if tr.is_sidex(tofpet_id[hits])]
    colorX=[df.iloc[event_id]['color'][hits] for hits in range(len(channels)) if tr.is_sidex(tofpet_id[hits])]
    hitsY=[tr.Mapping2D(tofpet_id[hits],channels[hits]) for hits in range(len(channels)) if not(tr.is_sidex(tofpet_id[hits]))]
    colorY=[df.iloc[event_id]['color'][hits] for hits in range(len(channels)) if not(tr.is_sidex(tofpet_id[hits]))]
    #print(colorX)
    if len(hitsX)>1 and len(hitsY)>1: ## Some events doesn't have hits on one of the two sides and are thus not considered
        x0,tx,hits_index=tr.tracks(hitsX)
        y0,ty,hits_indey,=tr.tracks(hitsY)
        steps=100000
        z=np.linspace(1,9,steps)
        x=tx*(z-9)*2+x0
        y=ty*(z-9)*2+y0
        trackx=np.array([[x[i],(z[i]-1)*2] for i in range(len(x))])## Track projection on X0
        tracky=np.array([[y[i],(z[i]-1)*2] for i in range(len(x))]) ## Track projection on Y
        ## Chi_2 test for the tracks determined before
        chix=tr.chi_2(hitsX,trackx,hits_index)
        chiy=tr.chi_2(hitsY,tracky,hits_indey)
        for i in range(len(x)):
           if x[i] < 0 or x[i] > 50:
               x[i] = -1000
               y[i] = -1000
               z[i] = -1000
        for i in range(len(y)):
           if y[i] < 0 or y[i] > 50:
               x[i] = -1000
               y[i] = -1000
               z[i] = -1000           
        x = np.delete(x, np.argwhere(x == -1000))
        y = np.delete(y, np.argwhere(y == -1000))
        z = np.delete(z, np.argwhere(z == -1000))
        trackx=np.array([[x[i],(z[i]-1)*2] for i in range(len(x))])## Track projection on X0
        tracky=np.array([[y[i],(z[i]-1)*2] for i in range(len(x))]) ## Track projection on Y

####                    GRAPHICAL DISPLAY OF THE EVENT              #########
        if (chix and chiy):
            Visual_Presentation(hitsX, hitsY,trackx,tracky,colorX,colorY) # Projective display on the 2 sides of the ECAL
        else:
            print('A track was not satisfying')