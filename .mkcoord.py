#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 22:32:15 2017

@author: xzz
"""

from astropy.stats import sigma_clipped_stats
import  astropy.io.fits as fits
import re
import numpy as np
import sys
import os
os.chdir('..')
f=open('llist')
f2=open('images.shift','w')
l1=re.sub('\n','',f.readline())
l1=re.sub('.f','-bdf.f',l1)

f2.write('0.0   0.000\n')
for i in f.readlines():
    f2.write('0.0   0.000\n')
f2.close()
f.close()

hdu = fits.open(l1)
data0 = hdu[0].data
size=data0.shape
(xmin)=int(size[1]/3)
ymin=int(size[0]/3)
(xmax)=int(size[1]/3)*2
ymax=int(size[0]/3)*2
data=data0[ymin:ymax,xmin:xmax]
mean, median, std = sigma_clipped_stats(data, sigma=3.0, iters=5)   
from photutils import DAOStarFinder

threshold=100.*std
daofind = DAOStarFinder(fwhm=4.0, threshold=threshold)    
sources = daofind(data - median)   

cnt=0

while len(sources)<4 or len(sources)>20:
    cnt+=1
    if len(sources)<4 :
        
        threshold/=2
        daofind = DAOStarFinder(fwhm=4.0, threshold=threshold)    
        sources = daofind(data - median)    
        
    else:
        sources.sort(keys='flux')
        sources = sources[:10]

    if cnt>5: 
        sys.exit(1)

print("threshold=",threshold)
f=open('images.coord','w')
for line in sources:
    x=xmin+line[1];y=ymin+line[2]
    f.write(str(x)+' '+ str(y)+'\n')
print(sources)
f.close()

import matplotlib.pyplot as plt
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from photutils import CircularAperture
positions = (sources['xcentroid'], sources['ycentroid'])
apertures = CircularAperture(positions, r=4.)
norm = ImageNormalize(stretch=SqrtStretch())
plt.imshow(data, cmap='Greys', origin='lower', norm=norm)
apertures.plot(color='blue', lw=1.5, alpha=0.5)

