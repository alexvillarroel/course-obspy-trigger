
from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime
from obspy.core import read
client = Client('iris')
t=UTCDateTime(2017,1,1,0,0,0)
data = client.get_waveforms('C1','BI05','--','HHZ',t,t+3600.)

# #crear datos
# data.write('test.mseed',format='MSEED')
# data2 = read('test.mseed',format='MSEED')
# data[0].data
# #data.plot()

# #cortar
# t1=UTCDateTime(2018,1,1,0,0,0.)
# t2=UTCDateTime(2018,1,1,0,15,0.)
# T=t2-t1
# cut =data.slice(starttime=t1,endtime=t2)
# cut1 =data.slice(starttime=t1,endtime=t2)
# #cut.plot()
# print cut[0].data.mean()
# cut.detrend(type='demean')
# print cut[0].data.mean()

# from copy import deepcopy as cp
# cut_copy =cp(cut)
# cut_copy.filter('lowpass',freq=1,corners=1)
# #cut_copy.plot()

#download from geofon and iris
from obspy.clients.fdsn import Client 
client1=Client('GFZ')
client2=Client('iris')
data1=client1.get_waveforms('CX', 'PB01', '--', 'HHZ',t, t+3600.)
data2=client2.get_waveforms('C1', 'BI05', '--', 'HHZ',t, t+3600.)
