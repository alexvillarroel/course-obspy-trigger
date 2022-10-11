#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 13:57:35 2020

@author: pablo
"""
import matplotlib
from obspy.core import read
from obspy.core import UTCDateTime
from obspy.signal import trigger
from obspy.signal.trigger import classic_sta_lta
t= UTCDateTime(2017,4,24,0,0,0)
t2= UTCDateTime(2017,4,25,0,0,0)
from obspy.clients.fdsn import Client
client = Client('iris')
data = client.get_waveforms('C1','VA05','--','HHZ',t,t2)
t3= UTCDateTime(2017,4,24,21,45)
t4= UTCDateTime(2017,4,24,22,00)
ff=data.slice(starttime=t3,endtime=t4)
#%%
cft=trigger.classic_sta_lta(ff[0].data,70,1500)

trigger.plot_trigger(ff[0],cft,6.75,0.2)
#%%
val = trigger.trigger_onset(cft,6.75,0.2)/data[0].stats.sampling_rate

for i in range(0,val.size/2):
    triggeron=ff[0].stats.starttime+ val[i,0]
    triggeron1=ff[0].stats.starttime+ val[i,1]
    triggeron='%4i/%02i/%02i %02i:%02i:%02i' % (triggeron.year, triggeron.month,triggeron.day,triggeron.hour,triggeron.minute,triggeron.second)
    triggeron1=' %02i:%02i:%02i' % (triggeron1.hour,triggeron1.minute,triggeron1.second)
    print ff[0].stats.station,triggeron, triggeron1
#%%