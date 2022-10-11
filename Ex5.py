#!/usr/bin/env python

from obspy.signal import trigger
from obspy.core import Stream, read, UTCDateTime
from obspy.clients.fdsn import Client
from copy import deepcopy as cp
import cPickle
#%%
client1 = Client('GFZ')
#%%
stations = ['PATCX','HMBCX','PB01','PB02','PB03','PB04','PB07','PB09']
t1 = UTCDateTime(2015,1,1,0,0,0)

#define empty stream, then fill it with data; data already gets filtered here
day1 = Stream()
for j in stations:
    dat = client1.get_waveforms('CX',j,'--','HHZ',t1,t1+86400.)
    dat.detrend(type='demean')
    dat.filter('bandpass',freqmin=0.5,freqmax=5.,corners=2)
    for i in dat:
        day1.append(i)
#%%
#pickling for later re-use
cPickle.dump(day1,open('Stream.bin','wb'))
#%%
day1 = cPickle.load(open('Stream.bin','rb'))

#coincidence trigger
output = trigger.coincidence_trigger('recstalta',5.,1,day1,5,details=True,sta=0.8,lta=12)

print str(len(output))+' Events found!'
#%%
outfile = open('Events.txt','w')
#outfileS = open('Events_S_wave.txt','w')
for j in output: #loop over events
    #write event separator
    outfile.write('#'*40)
    outfile.write('\n')
   # outfileS.write('#'*40)
   # outfileS.write('\n')
    #extract approx. origin time and stations
    traces = j['stations']
    timeX = j['time']
    #loop over stations
    for tr in traces:
        data = day1.select(station=tr)
        #cut out data segment
        sl = data.slice(starttime=timeX-20,endtime=timeX+90)
        #run STA/LTA
        cft = trigger.recursive_sta_lta(sl[0].data,80,1200)
        #get trigger alerts
        on_off = trigger.trigger_onset(cft,5,1)
        print on_off
        if len(on_off) > 1: #more than one trigger alert in the short segment
            print 'Warning: more than one alert'
        try: #take first alert
            alert = timeX -20 + (on_off[0][0]/sl[0].stats.sampling_rate)
            #string formatting for output
            datestr = '%4i/%02i/%02i' % (alert.year,alert.month,alert.day)
            timestr = '%02i:%02i:%05.2f' % (alert.hour,alert.minute,(alert.second+(alert.microsecond/1e6)))
          #  outfile.write(tr+' P'+'  '+datestr+' '+timestr+'\n')
        except: #no content in on_off
            continue

	#here we now try to look for S
    	data_E= client1.get_waveforms('CX',tr,'--','HHE',alert +2.,alert+60)
        data_E.detrend(type='demean')
        data_E.filter('bandpass',freqmin=0.1,freqmax=5.,corners=2)
        cft_E=trigger.recursive_sta_lta(data_E[0],40,300)
        on_off_E = trigger.trigger_onset(cft_E,3,0.5)
        print on_off_E 
       # trigger.plot_trigger(data_E[0],cft_E,3,0.5)
        try:
            alert_S = data_E[0].stats.starttime + (on_off_E[0][0]/data_E[0].stats.sampling_rate)
            datestr_S = '%4i/%02i/%02i' %(alert_S.year,alert_S.month,alert_S.day)
            timestr_S = '%02i:%02i:%05.2f' %(alert_S.hour,alert_S.minute, (alert_S.second + (alert_S.microsecond/1e6)))
            outfile.write (tr +'P'+ str(alert.timestamp) +' '+'S' + ' ' + str(alert_S.timestamp) + '\n')
        except:  
            outfile.write(tr + 'P' + ' ' + str(alert.timestamp) +'\n')  #no content in on_off_E  
            #continue
        
outfile.close()





