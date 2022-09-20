#!/usr/bin/env python3

## Time calibration of the channels of the PCB
import pandas as pd
import uproot
import uproot3
import numpy as np
import track_time_calibration as ttc
import Preparation as prep
import statistics as st
import functions_ttc as ftc
import cProfile
import Root_files_addition as rfa


## Look for the events where the reference channel is present

## ref corresponds to the reference SiPM properties. Its tofpet-channel and tofpet-id, 
    ##to exclude corresponds to the Reference SiPM position in the array of SiPMS, Initially delay is set equal to zero, as this is the delay of 
    ##the reference SiPM. Nonetheless, it is then modified based on the needd of the program, electronic_delay is in fact an array containing all
    ##the relative delays, once again t_entry is a bit misleading as it describes the value tstamp_ref-tscint_ref-tcal_ref
    
def ref_chosed (ref,to_exclude,delay,elec_delay,t_entries):
    ch_ref=ref[0] ## the reference channel to be isoalted
    t_id_ref=ref[1] ## tofpet id of the reference channel
    dt=[[] for i in range(length)]
    for track_id in range(nb_tracks):
        channels=df['tofpet_channel'].iloc[tracks_id[track_id]]## we use that because there is no perfect correspondance between the track id and the events
                                                               ## as recorded by the tofpet
        tofpet=df['tofpet_id'].iloc[tracks_id[track_id]]## it is convoluted, a perver way to quantify it algorithmically
        t_stamp=df['timestamp'].iloc[tracks_id[track_id]]*6.25

        tr_param=tracks['track_param'].loc[track_id][1:-1].split(',')##break
        tr_param=[float(tr) for tr in tr_param]## convert
        index_y=tracks['index_y'].loc[track_id][1:-1].split(',')
        index_y=[int(y) for y in index_y]
        index_x=tracks['index_x'].loc[track_id][1:-1].split(',')
        index_x=[int(x) for x in index_x]

        if ttc.is_sidex(t_id_ref):
            hits_other_side=[ttc.Mapping2D(tofpet[i],channels[i]) for i in index_y]  ## we find the position of the hits on the y axis relative to the SiPM under question
        else:
            hits_other_side=[ttc.Mapping2D(tofpet[i],channels[i]) for i in index_x]  ## we find the position of the hits on the x axis relative to the SiPM under question


        suitable, t_entry = ftc.suitable_track([ch_ref,t_id_ref],channels,tofpet,hits_other_side,t_stamp,tr_param)
        if suitable:
            if ttc.is_sidex(t_id_ref):
                for ind in range(len(index_x)):
                    index=index_x[ind]
                    dsc_=dsc_x[track_id][ind]
                    if not(np.isnan(dsc_)) and not(ttc.position_in_array(channels[index],tofpet[index],'X') in to_exclude): ## eliminate the case where there is no side correspondance
                                                                                                                            ## eliminate the case of the reference point
                        if t_entries[track_id]==0:
                            t_entries[track_id]=t_entry
                        dcal_=dcal_x[track_id][ind]
                        chan=channels[index]
                        tof_id=tofpet[index]
                        t_ch=t_stamp[index]-delay
## This part of the algorithm is correct. Delay is a variable in order to be able each time to reference back to the real delay of the reference point. Thus at the begining
## is indeed zero, so negligeable but as we change reference point the intrinsic delay is modified. 
                        pos=ttc.position_in_array(chan,tof_id,'X')
                        t=t_entry+dsc_/csc+dcal_/c
                        dt[pos].append(t_ch-t)
            else:
                for ind in range(len(index_y)):
                    index=index_y[ind]
                    dsc_=dsc_y[track_id][ind]
                    if not(np.isnan(dsc_)) and not(ttc.position_in_array(channels[index],tofpet[index],'Y') in to_exclude): ## eliminate the case where there is no side correspondance
                        if t_entries[track_id]==0:
                            t_entries[track_id]=t_entry
                        dcal_=dcal_y[track_id][ind]
                        chan=channels[index]
                        tof_id=tofpet[index]
                        t_ch=t_stamp[index]-delay
                        pos=ttc.position_in_array(chan,tof_id,'Y')
                        t=t_entry+dsc_/csc+dcal_/c
                        dt[pos].append(t_ch-t)
                     
   electronic_delay=[np.mean(dt[pos]) if (len(dt[pos])>50 and not(pos in to_exclude))  else elec_delay[pos]  for pos in range(length)]
    ## we don't actually need the mean. We shall get the raw data and do ourselves the fitting
    #print(elec_delay,t_entries)
    return electronic_delay,t_entries  ## SSOSS       


need_prep=False

c=30 ## speed of light
csc=17.526 ## speed of light in the fibre as cm/ns
length=192

df=rfa.merger(['/home/ecal/Documents/scripts/Analysis/Data/10h/data_0000.root', 
               '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0001.root',
               '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0002.root',
               '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0003.root', 
               '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0004.root',
               '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0005.root', 
               '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0006.root',
               '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0007.root',
               '/home/ecal/Documents/scripts/Analysis/Data/10h/data_0008.root' ])
tracks=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Track_reconstruction/tracks.csv')## [indexx, indexy, truck-parameter, event_id]
tracks_id=tracks['track_id'] ## The id number of a track, not the id of the event corresponding to the track, they are not the same
nb_tracks=len(tracks_id)

if need_prep:
    print('Preparation started')
    prep.Preparation('X',df)
    prep.Preparation('Y',df)
    print('Preparation finished')


dsc_y_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dsc_Y.csv')## distance scintillator
dcal_y_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dcal_Y.csv')## Distance travelled between layers 
dsc_x_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dsc_X.csv')
dcal_x_temp=pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/dcal_X.csv')

dsc_x=[ list(dsc_x_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]
dcal_x=[ list(dcal_x_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]
dsc_y=[ list(dsc_y_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]
dcal_y=[ list(dcal_y_temp.iloc[track_id])[1:] for track_id in range(nb_tracks)]


for i in range(2):

    # Reference Channel on the X side
    ch_ref=62-i
    t_id_ref=4
    side='X'
    delay=0

    # Refernece Channcel on the Y side
    ch_ref_y=62-i ## channel-id
    t_id_ref_y=6 ##tofpet-id
    side='Y'
    delay=0


    electronic_delay_x=np.zeros(length)
    electronic_delay_x[ttc.position_in_array(ch_ref,t_id_ref,'X')]=delay ###Probably redundant
    to_exclude=[ttc.position_in_array(ch_ref,t_id_ref,'X')] ### maybe redundant
    already_used=[ttc.position_in_array(ch_ref,t_id_ref,'X')] ## Array indicating which SiPMs have already been used as references

    electronic_delay_y=np.zeros(length)
    electronic_delay_y[ttc.position_in_array(ch_ref_y,t_id_ref_y,'Y')]=delay ##Probably redundant 
    to_exclude_y=[ttc.position_in_array(ch_ref_y,t_id_ref_y,'Y')]## Maybe redudant, because has the same functionality as the already used factor
    already_used_y=[ttc.position_in_array(ch_ref_y,t_id_ref_y,'Y')] ## Array indicating which SiPMs have already been used as references
    # print(electronic_delay_y)
    # print(to_exclude_y)
    # print(already_used_y)
    # print("Now we pass to the while loops")
    t_entries=np.zeros(nb_tracks)

    while len(to_exclude)<192: ## we set this condtion, representing the delay of each side. The algorithm terminates once the delay of each SiPM has benn evaluated.
        electronic_delay_x,t_entries=ref_chosed([ch_ref,t_id_ref],to_exclude,delay,electronic_delay_x,t_entries)
        to_exclude.extend([i for i in range(length) if (not(i in to_exclude) and electronic_delay_x[i]!=0)])## to exclude is not actually to exclude, it is rather 
        ## simply a the SiPMs that have been activated taken into account this particular reference SiPM. 
        channels_ref_cand,t_id_ref_cand=ftc.to_ch_t_id(to_exclude,already_used,'X') 
        ## This function has a rather misleading functionality. It aims to go over the list of the SiPMs and check which SiPMs have not been used already as references. 
        ## allowing the deployment of the following function which in fact determines the next reference channel. 
        ## In order to determine the new reference points we use the candiates lists plus the previous ones 
        ch_ref,t_id_ref=ftc.find_new_ref(channels_ref_cand,t_id_ref_cand,[ch_ref,t_id_ref])
        ## Next station, the marking of the used channel. 
        already_used.append(ttc.position_in_array(ch_ref,t_id_ref,'X'))
        ## Now the dealy of the system is equal to the dealy of this particular SiPM. We carry this dealy residual to be added for the next cycle. S
        ## SOS NOW WE FOUND THE LOGICAL ERROR. THE DELAY OF THE INITIAL REFERENCE CHANNEL WAS SET TO BE EQUAL TO ZERO. BUT IT MIGHT VERY WELL BE FAR FROM THE REAL ZERO. 
        delay=electronic_delay_x[ttc.position_in_array(ch_ref,t_id_ref,'X')]
        print('Still have to add '+str(192-len(to_exclude))+' SiPMs for side X')


    while len(to_exclude_y)<191: ## SEE THE PREVIOUS LINES
        electronic_delay_y,t_entries=ref_chosed([ch_ref_y,t_id_ref_y],to_exclude_y,delay,electronic_delay_y,t_entries)
        to_exclude_y.extend([i for i in range(length) if (not(i in to_exclude_y) and electronic_delay_y[i]!=0)])
        channels_ref_cand,t_id_ref_cand=ftc.to_ch_t_id(to_exclude_y,already_used_y,'Y')
        ch_ref_y,t_id_ref_y=ftc.find_new_ref(channels_ref_cand,t_id_ref_cand,[ch_ref_y,t_id_ref_y])
        already_used_y.append(ttc.position_in_array(ch_ref_y,t_id_ref_y,'Y'))
        delay=electronic_delay_y[ttc.position_in_array(ch_ref_y,t_id_ref_y,'Y')]
        print('Still have to add '+str(191-len(to_exclude_y))+' SiPMs for side Y')

    #print(electronic_delay_x)
    #print(electronic_delay_y)

    # Find delay of the SiPM on side Y wrt to the one on side X
    ch_ref=62
    t_id_ref=4
    side='X'
    delay=0
    dt=[]
    for track_id in range(nb_tracks):
        channels=df['tofpet_channel'].iloc[tracks_id[track_id]]## all the tofpet channels of the hits which constitute the track under question
        tofpet=df['tofpet_id'].iloc[tracks_id[track_id]]## all the tofpet ids of hits which constitute the track under questio
        index_y=tracks['index_y'].loc[track_id][1:-1].split(',')
        index_y=[int(y) for y in index_y]## indices of the hits corresponding to the y side
        index_x=tracks['index_x'].loc[track_id][1:-1].split(',')
        index_x=[int(x) for x in index_x]## indices of the hits corresponding to the x side
        channels_x=channels[index_x]## only the channels which correspond to the x side
        channels_y=channels[index_y]## only the channels which correspond to the y side
        t_id_x=tofpet[index_x]## only the tofpet-id which correspond to the x side
        t_id_y=tofpet[index_y]## only the tofpet-id which correspond to the y side
        if any([t_id_x[i]==t_id_ref and channels_x[i]==ch_ref for i in range(len(channels_x))]) and any([t_id_y[i]==t_id_ref_y and channels_y[i]==ch_ref_y for i in range(len(channels_y))]):## simply asks if in that list we have the in the track both reference channels activated
            t_stamp=df['timestamp'].iloc[tracks_id[track_id]]*6.25
            ind_x=np.argwhere([t_id_x[i]==t_id_ref and channels_x[i]==ch_ref for i in range(len(channels_x))])[0][0]## we find the index that actually corresponds the reference channel of the side x
            ind_y=np.argwhere([t_id_y[i]==t_id_ref_y and channels_y[i]==ch_ref_y for i in range(len(channels_y))])[0][0]## we find the index corresponding to the reference channel of the side y
            t_stamp_x=t_stamp[index_x[ind_x]]## we find the actual timestamp of the reference channel x
            t_stamp_y=t_stamp[index_y[ind_y]]## we find the actual timestamp of the reference channel y
            dcal_x_ref=dcal_x[track_id][ind_x]## we find the actual dcal of the reference channel x
            dcal_y_ref=dcal_y[track_id][ind_y]## we find the actual dcal of the reference channel x
            dsc_x_ref=dsc_x[track_id][ind_x]## we find the actual dscnt of the reference channel x
            dsc_y_ref=dsc_y[track_id][ind_y]## we find the actual dscnt of the reference channel x
            t_entry=t_stamp_x-dcal_x_ref/c-dsc_x_ref/csc## it is the relative of the relative okay we need clarifications
            dt.append(t_stamp_y-t_entry-dcal_y_ref/c-dsc_y_ref/csc)
    delay_y=np.mean([x for x in dt if not(np.isnan(x))])
    print(delay_y)
    pd.DataFrame(electronic_delay_x).to_csv('electronic_delay_x.csv')

    pd.DataFrame(electronic_delay_y-delay_y).to_csv('electronic_delay_y.csv')
    pd.DataFrame(t_entries).to_csv('t_entries.csv')



    ###### TEST1 together with the previous one #######

    c=30 ## speed of light
    csc=17.526 ## speed of light in the fibre as cm/ns
    length=192

    # Channel that will be taken as a refence
    ch_ref=62-i
    t_id_ref=4
    side='X'
    delay=0

    a=pd.read_csv('electronic_delay_x.csv')
    electronic_delay_x=np.array(a[a.columns[1]])
    a=pd.read_csv('electronic_delay_y.csv')
    electronic_delay_y=np.array(a[a.columns[1]])
    a=pd.read_csv('t_entries.csv')
    t_entries=np.array(a[a.columns[1]])
    det_time_x=[[] for i in range(length)]
    det_time_y=[[] for i in range(length)]
    for track_id in range(nb_tracks):
        channels=df['tofpet_channel'].iloc[tracks_id[track_id]]
        tofpet=df['tofpet_id'].iloc[tracks_id[track_id]]
        t_stamp=df['timestamp'].iloc[tracks_id[track_id]]*6.25
        t_entry=t_entries[track_id]
        tr_param=tracks['track_param'].loc[track_id][1:-1].split(',')
        tr_param=[float(tr) for tr in tr_param]
        index_y=tracks['index_y'].loc[track_id][1:-1].split(',')
        index_y=[int(y) for y in index_y]
        index_x=tracks['index_x'].loc[track_id][1:-1].split(',')
        index_x=[int(x) for x in index_x]


        for ind in range(len(index_x)):
            index=index_x[ind]
            dsc_=dsc_x[track_id][ind]
            if not(np.isnan(dsc_)):
                dcal_=dcal_x[track_id][ind]
                chan=channels[index]
                tof_id=tofpet[index]
                t_ch=t_stamp[index]
                pos=ttc.position_in_array(chan,tof_id,'X')
                delay=electronic_delay_x[pos]
                   ## SOS That line was erroneous. WE SHALL ALWAYS BEAR IN MIND THE FACT THAT WE ARE AFTER THE RESIDUALS. THIS ONE RIGHT HERE WAS WRONG AS 
                   ## IT WAS RETURNING THE 
                det_time_x[pos].append(t_ch-dsc_/csc-dcal_/c-delay)

        for ind in range(len(index_y)):
            index=index_y[ind]
            dsc_=dsc_y[track_id][ind]
            if not(np.isnan(dsc_)):
                dcal_=dcal_y[track_id][ind]
                chan=channels[index]
                tof_id=tofpet[index]
                t_ch=t_stamp[index]
                pos=ttc.position_in_array(chan,tof_id,'Y')
                delay=electronic_delay_y[pos]
                det_time_y[pos].append(t_ch-dsc_/csc-dcal_/c-t_entry-delay)

    meanx=np.zeros(192)
    meany=np.zeros(192)


    # for i in range (192):
    #     plt.figure()
    #     plt.hist(det_time_y[i],100)
    #     plt.title(str(np.mean(det_time_y[i])))
    #     plt.xlabel("Relative residual time")
    #     plt.ylabel("Number of events")
    #     plt.grid("on")
    #     plt.savefig('/home/ecal/Documents/scripts/Analysis/Time_calibration/Graphs/refxchannel'+str(i)+'.png',dpi=300)
    #     meany[i]=np.mean(det_time_y[i])

    for j in range (192):
        rfa.Gaussian_fit(det_time_y[j],'refx'+str(62-i)+'channel'+str(j))
        rfa.Gaussian_fit(det_time_y[j],'refy'+str(62-i)+'channel'+str(j))
