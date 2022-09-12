#!/usr/bin/env python3
import uproot
import uproot3
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt
import mplhep as hep
from itertools import combinations
import mplhep as hep
from vpython import *
from time import *
import turtle
from mpl_toolkits.mplot3d import Axes3D
plt.style.use([hep.style.LHCb])
from datetime import datetime
import track_reconstruction as tr
import sys
sys.path.insert(1, '/home/ecal/Documents/scripts/Analysis/Time_calibration')
import Root_files_addition as rfa

## This code determine muon tracks using Hough transform on the hits projected on each side of the ECAL.
## This code works for events with only one track.


#root_file =  '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0000.root'
#Tname = 'board_57'
#br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel', 'tac']#, 't_coarse', 't_fine', 'timestamp', 'v_coarse', 'v_fine', 'value', 'timestamp_cal_chi2', 'timestamp_cal_dof', 'value_cal_chi2', 'value_cal_dof', 'value_saturation']
df=rfa.merger(['/home/ecal/Documents/scripts/Analysis/Data/10h/data_0000.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0001.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0002.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0003.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0004.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0005.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0006.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0007.root', '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0008.root' ])


running=1

#####   FUNCTION FOR GRAPHICAL DISPLAY OF THE TRACK AND THE HITS PROJECTED ON EACH SIDE #######
def make_grid_3D(xmax,dx):
    for x in range(-xmax,xmax+dx,dx):
        curve(pos=[vector(x,xmax,0),vector(x,-xmax,0)],color=color.white,radius=0.05)
    for y in range(-xmax,xmax+dx,dx):
        curve(pos=[vector(xmax,y,0),vector(-xmax,y,0)],color=color.white,radius=0.05)
    for x in range(-xmax,xmax+dx,dx):
        curve(pos=[vector(x,0,xmax),vector(x,0,-xmax)],color=color.white,radius=0.05)
    for z in range(-xmax,xmax+dx,dx):
        curve(pos=[vector(xmax,0,z),vector(-xmax,0,z)],color=color.white,radius=0.05)
    for y in range(-xmax,xmax+dx,dx):
        curve(pos=[vector(0,y,xmax),vector(0,y,-xmax)],color=color.white,radius=0.05)
    for z in range(-xmax,xmax+dx,dx):
        curve(pos=[vector(0,xmax,z),vector(0,-xmax,z)],color=color.white,radius=0.05)
    arrow(pos=vector(24,0,0),length=5,axis=vector(1,0,0),color=color.blue)
    arrow(pos=vector(0,24,0),length=5,axis=vector(0,1,0),color=color.blue)
    arrow(pos=vector(0,0,24),length=5,axis=vector(0,0,1),color=color.blue)

    text(text="X",
         pos=vector(24,0,0),
         height=3,
         depth=0.1,
         color=color.blue)
    text(text="Y",
         pos=vector(0,24,0),
         height=3,
         depth=0.1,
         color=color.blue)
    text(text="Z",
         pos=vector(0,0,27),
         height=3,
         depth=0.1,
         color=color.blue,
         axis=vector(0,0,-1))
    return


def Run(b):
    global running
    if running==True:
        b.text="Run"
        running=0
    else:
        b.text="Pause"
        running=1

scene.width=2000
scene.height=900
scene.background = color.cyan
bottom = box(pos=vector(12*1.6+0.8, 0, 12*1.6+0.8), color=color.red, length=24*1.6+0.8, width=24*1.6+0.8, height=0.5)
cubex_dictionary = {}
for i in range(1, 25):
    for j in range(1, 9):
        cubex_dictionary["mybox1" + str(i) + str(j)] = box(pos=vector(1.6*i+0.8, 2*j-1, 0), length=1.6*0.8, height=2*0.8,width=0.01, color=color.black, shininess=False)
#        distant_light(direction=vector(i, j, 0), color=color.white)
distant_light(direction=vector(0, 0, 0), color=color.white)
distant_light(direction=vector(39, 18, 0), color=color.white)

cubey_dictionary = {}
for i in range(1, 25):
    for j in range(1, 9):
        cubey_dictionary["mybox2" + str(i) + str(j)] = box(pos=vector(0, 2*j-1, 1.6*i+0.8), length=0.01, height=2*0.8,width=1.6*0.8 , color=color.black, shininess=False)
        #distant_light(direction=vector(i, j, 0), color=color.white)
distant_light(direction=vector(0, 0, 0), color=color.white)
distant_light(direction=vector(39, 18, 0), color=color.white)

text(text = "Side X",
    pos = vector(12, 9*2, 0),
    height = 3,
    depth = 0.1,
    color =color.yellow)
text(text = "Side Y",
    pos = vector(0, 9*2, 24),
    height = 3,
    depth = 0.1,
    color =color.yellow,
    axis=vector(0,0,-1))

def Visual_Presentation3D(track):
    c1=curve(pos=[vector(track[-1][0],track[-1][2],track[-1][1]),vector(track[0][0],track[0][2],track[0][1])],radius=0.5,color=color.green)
    temp = 0
    samples=100
    while temp < samples:
        rate(100)
        if(running==1):
         temp = temp + 1
        pass
    c1.visible=False
    c1.delete()
                                ##############


# Extract the data and transform it into a dataframe
#with uproot.open(root_file) as tree:
    #dict_ecal = tree[Tname].arrays(br_list_data, library="np")


button(text="Pause",pos=scene.title_anchor,bind=Run)


#df = pd.DataFrame.from_dict(dict_ecal).query('n_hits>6')
#df=df.query('n_hits<18')
nb_events=12
steps=100000
for event_id in range(len(df)):
    t=datetime.now()
    channels=df.iloc[event_id]['tofpet_channel']
    tofpet_id=df.iloc[event_id]['tofpet_id']
    hitsX=[tr.Mapping2D(tofpet_id[hits],channels[hits]) for hits in range(len(channels)) if tr.is_sidex(tofpet_id[hits])]
    hitsY=[tr.Mapping2D(tofpet_id[hits],channels[hits]) for hits in range(len(channels)) if not(tr.is_sidex(tofpet_id[hits]))]
    if len(hitsX)>1 and len(hitsY)>1: ## Some events doesn't have hits on one of the two sides and are thus not considered
        x0,tx,hits_index=tr.tracks(hitsX)
        y0,ty,hits_indey,=tr.tracks(hitsY)
        z=np.linspace(1,9,steps)
        x=tx*(z-9)*2+x0
        y=ty*(z-9)*2+y0
## Find the tracks using 2 points 
        trackx=[[x[i],(z[i]-1)*2] for i in range(steps)]## Track projection on X
        tracky=[[y[i],(z[i]-1)*2] for i in range(steps)] ## Track projection on Y
        track=[[x[i],y[i],(z[i]-1)*2] for i in range(steps)]
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
        if chix and chiy:
            #make_grid_3D(24,1)
            Visual_Presentation3D(track)
        else:
            print('A track was not satisfying')
