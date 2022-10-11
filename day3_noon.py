#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 15:34:33 2020

@author: pablo
"""


import hypo71
import matplotlib.pyplot as plt
pck= hypo71.prepare_picks('peaks.txt')
valx=[]
valy=[]
valz=[]
outfile = open('eventsa.txt','w')
for j in range(len(pck)):
    print j
    #a = hypo71.prepare_picks('picks.txt')
    hypo71.generate_input('.',pck[j+1]['hypolines'],'info_file','velmod.hdr')
    hypo71.call_Hypo71('.')
    out=hypo71.read_output('.')
    valx.append(out['ev_lat'])
    valy.append(out['ev_lon'])
    valz.append(out['ev_depth'])
    hypo71.write_pha(out)
    #outfile.write(str())
outfile.close()
#%%
x=[]
y=[]
z=[]
for i in range(101):
    x.append(float(valx[i]))
    y.append(float(valy[i]))
    z.append(float(valz[i]))
#%%
plt.figure()
plt.plot(x,y,'o')
plt.figure()
plt.plot(x,z,'o')
plt.figure()
plt.plot(y,z,'o')