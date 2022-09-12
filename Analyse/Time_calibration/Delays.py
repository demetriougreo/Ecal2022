#!/usr/bin/env python3

import pandas as pd
import matplotlib
import numpy as np
from matplotlib import pyplot as plt

delay0 = pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/Electronic_delay_0.csv')
delay1 = pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/Electronic_delay_1.csv')
delay2 = pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/Electronic_delay_2.csv')
delay3 = pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/Electronic_delay_3.csv')
delay4 = pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/Electronic_delay_4.csv')
delay5 = pd.read_csv('/home/ecal/Documents/scripts/Analysis/Time_calibration/Electronic_delay_5.csv')

delays=[[] for i in range(384)]
for i in range(384):
    arr1=delay0.iloc[i]
    arr2=delay1.iloc[i]
    arr3=delay2.iloc[i]
    arr4=delay3.iloc[i]
    arr5=delay4.iloc[i]
    arr6=delay5.iloc[i]
    delays[i]=np.concatenate((arr1, arr2,arr3,arr4 , arr5 ,  arr6))


for i in range(384):
    plt.figure()
    plt.hist(delays[i],40)
    plt.xlabel("Angles [rad]")
    plt.ylabel("Number of tracks")
    plt.grid()
    plt.show()