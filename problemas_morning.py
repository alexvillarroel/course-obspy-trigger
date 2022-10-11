#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 11:07:23 2020

@author: pablo
"""


from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime
from obspy.core import read
from copy import deepcopy as cp

client = Client('iris')

t1=UTCDateTime(2017,1,1,18,3,0.)
t12=UTCDateTime(2017,1,1,18,5,0.)

t2=UTCDateTime(2017,4,24,4,47,0.)
t22=UTCDateTime(2017,4,24,4,52,0.)

data1 = client.get_waveforms('C1','VA05','--','HH?',t1,t12)
data2 = client.get_waveforms('C1','VA05','--','HH?',t2,t22)   

data1.plot()
data2.plot()

d10=cp(data1)
d10.detrend(type='demean')

d20=cp(data2)
d20.detrend(type='demean')

d11=cp(d10)
d12=cp(d10)
d13=cp(d10)
d14=cp(d10)
d15=cp(d10)
d16=cp(d10)
d17=cp(d10)

d21=cp(d20)
d22=cp(d20)
d23=cp(d20)
d24=cp(d20)
d25=cp(d20)
d26=cp(d20)
d27=cp(d20)

d11.filter('highpass',freq=1,corners=2)
d12.filter('highpass',freq=5,corners=2)
d13.filter('lowpass',freq=1,corners=2)
d14.filter('lowpass',freq=5,corners=2)
d15.filter('bandpass',freqmin=0.5,freqmax=5,corners=2)
d16.filter('bandpass',freqmin=0.1,freqmax=1,corners=2)
d17.filter('bandpass',freqmin=5,freqmax=20,corners=2)

d21.filter('highpass',freq=1,corners=2)
d22.filter('highpass',freq=5,corners=2)
d23.filter('lowpass',freq=1,corners=2)
d24.filter('lowpass',freq=5,corners=2)
d25.filter('bandpass',freqmin=0.5,freqmax=5,corners=2)
d26.filter('bandpass',freqmin=0.1,freqmax=1,corners=2)
d27.filter('bandpass',freqmin=5,freqmax=20,corners=2)
#ut_copy.filter('lowpass',freq=1,corners=1)
#%%
import obspy
stat=open('stations','r')
XX=stat.readlines()
o=0
lat1=-32.115
lon1=-71.175

for i in XX:
    sta,lon,lat =i.split()
    LAT=float(lat)
    o=o+1
    print o
    
    