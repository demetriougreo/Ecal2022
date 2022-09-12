#!/usr/bin/env python3

## Study the correlation between mean value and standard devitation of the muon event distribution 
# Using the datas obtained for the amplitude calibration
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt


df=pd.read_csv('QDC.csv')
df2=pd.read_csv('QDC2.csv')
m0=df['tac0']
m1=df['tac1']
s0=df['sigma0']
s1=df['sigma1']
m2=df['tac2']
m3=df['tac3']
s2=df['sigma2']
s3=df['sigma3']
plt.figure()
plt.title('Consider all events with more than 5 hits')
plt.scatter(m0,s0)
plt.scatter(m1,s1)
plt.scatter(m2,s2)
plt.scatter(m3,s3)
plt.savefig('all.png')
plt.show()
plt.clf()

m0=df2['tac0']
m1=df2['tac1']
s0=df2['sigma0']
s1=df2['sigma1']
m2=df2['tac2']
m3=df2['tac3']
s2=df2['sigma2']
s3=df2['sigma3']
plt.figure()
plt.title('Consider events with 5<hits<20')
plt.scatter(m0,s0)
plt.scatter(m1,s1)
plt.scatter(m2,s2)
plt.scatter(m3,s3)
plt.savefig('less_than_20.png')
plt.show()