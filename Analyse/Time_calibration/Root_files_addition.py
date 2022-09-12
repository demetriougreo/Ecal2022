#!/usr/bin/env python3

from heapq import merge
from tkinter import Y
import pandas as pd
import uproot
#import uproot3
import numpy as np
import track_time_calibration as ttc
from matplotlib import pyplot as plt
import Preparation as prep
import statistics as st
import ROOT

def merger(Array_of_paths):
    br_list_data = ['n_hits', 'tofpet_id', 'tofpet_channel', 'timestamp']#, 't_coarse', 't_fine', 'timestamp', 'v_coarse', 'v_fine', 'value', 'timestamp_cal_chi2', 'timestamp_cal_dof', 'value_cal_chi2', 'value_cal_dof', 'value_saturation']   
    df_general = pd.DataFrame(columns = br_list_data)
    for element in Array_of_paths:
        Tname = 'board_57'
        # Extract the data and transform it into a dataframe
        with uproot.open(element) as tree:
            dict_ecal = tree[Tname].arrays(br_list_data, library="np")
        ## REALLY IMPORTANT, THE TIME CALIBRATION MUST BE DONE USIGN THE SAME DATAFRAME AS THE ONE USED TO RECONSTRUCT THE TRACK

        df = pd.DataFrame.from_dict(dict_ecal).query('n_hits>6')
        df['path_id'] = element
        df=df.query('n_hits<18')
        #print(df)
        df_general=df_general.append(df)
    print(df_general)
    return df_general
## THUS FAR WE HAVE OPENED AND CREATED A GENERIC DATAFRAME ##


#Yey=merger(['/home/ecal/Documents/scripts/Analysis/Data/10h/data_0002.root','/home/ecal/Documents/scripts/Analysis/Data/10h/data_0001.root'])





import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numpy.random import normal
from scipy import stats
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from scipy.stats import norm


def gauss(x,amp,mu,sigma):
    return amp*np.exp(-(x-mu)**2/(2*sigma**2))

def Gaussian_fit(data,side):
    plt.figure()
    mean=np.average(data)
    variance=np.std(data)
    n,bins,patches=plt.hist(data,1000,range=(min(data),max(data)))
    y=n
    x=np.linspace(min(data),max(data),1000)
    indices = np.argwhere((x>= mean-1) & (x <= mean+1))
    x=x[indices]
    y=n[indices]
    y=y.flatten()
    x=x.flatten()
    popt,pcov=curve_fit(gauss, x, y, maxfev=200000, p0=(max(y),mean,variance))
    y=gauss(x,popt[0],popt[1],popt[2])
    plt.plot(x,y,color='r',linestyle='dashed')
    title = "Fit Values: {:.5f} and {:.5f}".format(popt[1], popt[2])
    plt.title(title)
    #setting the label,title and grid of the plot
    #print(indices)
    plt.xlabel("Residuals t$_{r}$[ns]")
    plt.ylabel("Number of activations")
    plt.grid("on")
    plt.savefig('/home/ecal/Documents/scripts/Analysis/Time_calibration/Graphs/channel'+str(side)+'.png',dpi=300)
    return popt[1]

Gaussian_fit(normal(loc=0, scale=1, size=200),-1000)