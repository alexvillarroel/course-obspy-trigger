#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 09:07:58 2020

@author: pablo
"""


from obspy.signal import trigger
from obspy.core import Stream, UTCDateTime
from obspy.clients.fdsn import Client
client = Client('GFZ')
t1 = UTCDateTime(2015,1,1,0,0,0)
st = Stream()
stations = ['PATCX','HMBCX','PB01','PB02','PB03','PB04','PB07','PB09']
#%%
for j in stations:
    data = client.get_waveforms('CX',j,'--','HHZ',t1,t1+86400.)
    st.append(data[0])
print(st)
#%%
import cPickle
cPickle.dump(st,open('stream.bin','wb'))
#%%
st = cPickle.load(open('stream.bin','rb'))
#%%
output=trigger.coincidence_trigger('recstalta', 2.1, 0.2, st, 6, sta=0.6,lta=10.)
print(len(output))
#%%
for i in range(0,len(output)):
    stat=output[i]['stations']
    tim=output[i]['time']
    tim='%4i/%02i/%02i %02i:%02i:%02i' %(tim.year, tim.month, tim.day,tim.hour , tim.minute, tim.second)
    print stat,tim  
#%%
    #Now we want determine exact arrival times for each stations 
    #For this, we can apply a simple STA/LTA on a small time window 
    #(discuss strategy). Try this out using plot_trigger()
    #to check if picks to are ok

#ff=data.slice(starttime=t3,endtime=t4)    
#cft=trigger.classic_sta_lta(ff[0].data,70,1500)
#trigger.plot_trigger(ff[0],cft,6.75,0.2)
from obspy.signal.trigger import classic_sta_lta
from obspy.core import Stream, UTCDateTime
from obspy.clients.fdsn import Client
client = Client('GFZ')
for i in range(0,len(output)):
    t0=output[i]['time']
    t1=output[i]['duration']
    t11 = UTCDateTime(2015,1,1,0,0,0)
    t2=t0+t1
    stat=output[i]['stations']
    print('#'*40)
    print('\n')
    for j in stat:
        data = client.get_waveforms('CX',j,'--','HHZ',t11,t11+86400.)
        ff=data.slice(starttime=t0-20,endtime=t2+90)
        cft=trigger.recursive_sta_lta(ff[0].data,60,1000)
        #trigger.plot_trigger(ff[0],cft,2.1,0.2)
        val = trigger.trigger_onset(cft,2.1,0.2) / data[0].stats.sampling_rate
        tim=ff[0].stats.starttime+val[0,0]
        #tim= %4i/%02i/%02i %02i:%02i:%02i' %(tim.year, tim.month, tim.day,tim.hour , tim.minute, tim.second)
        print j, tim
        



