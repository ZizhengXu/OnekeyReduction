#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 15:44:44 2017

@author: xzz
"""

from astropy.io import fits
import re
import os
import numpy as np
import scipy.stats as stats
from scipy.optimize import minimize
from numpy.random import normal
import random
os.chdir('..')
class deviation(object):
    """using img1 toalign img2, output deviation
    """
    def __init__(self,img2,img1,box=30):
#        self.img1=img1
        (self.xsize,self.ysize)=np.round(np.divide(img1.shape,3))
        self.d1=img1[int(self.xsize):int(self.xsize*2),int(self.ysize):int(self.ysize*2)]
        self.img2=img2
        self.cons={'type': 'ineq',
          'fun' : lambda x: np.array([x[0] - box]) and np.array([ box - x[0]]) and np.array([x[1] - box]) and np.array([ box - x[1]]) 
          }
        self.objf=1;self.optimx=[];
    def func(self,dx):
        d2=self.img2[int(self.xsize+dx[0]):int(self.xsize*2+dx[0]),int(self.ysize+dx[1]):int(self.ysize*2+dx[1])]
#        print(dx)
        return -stats.pearsonr(self.d1.reshape(-1),d2.reshape(-1))[0]
    def getminxy(self,box=30):
        cnt=0;maxc=min(box**2/30,100)
        while True:
            
            try:
                res = minimize(self.func, [random.randint(-box,box),random.randint(-box,box)],
                                      method='Powell', options={'disp': False}  )
            except ValueError:
                continue
            cnt+=1;tmp=self.func(res.x)
            if tmp<-0.9:
                print('finally:',tmp)
                return (res.x,0)
            if self.objf>tmp: 
                self.objf=tmp;self.optimx=res.x
                
            if cnt> maxc : 
                if self.objf<-0.3:
                    print('might not be best:',self.objf)
                    return (self.optimx,0)
                else: 
                    print('better recheck:',self.objf)
                    return (self.optimx,1)
        #,'maxiter':16,  constraints=self.cons  , options={'disp': True}  , ,tol=1e-10 constraints=self.cons,   
        
with open('llist') as f:
    file1=re.sub('.f','-bdf.f',f.readline().split('\n')[0])
     #reference
    files=[re.sub('.f','-bdf.f',line.split('\n')[0]) for line in f.readlines()]
     #to be aligned
    data1=fits.getdata(file1)
with open( 'coord.shift' ,'w') as f:
    f.write('0 0\n')
    os.system('cp '+file1+' '+re.sub('-bdf.f','-bdfa.f',file1))
    for file_ in files:
        data2=fits.getdata(file_)
        print('trying to align '+file_+':')
        instance=deviation(data2,data1)
        [dx,dy],flag=instance.getminxy()
        if flag:
            [dx,dy],flag=instance.getminxy(box=300)
        print(' result: ',-dy,'  , ',-dx)
        buff1=str(-dy)+' '+str(-dx)+'\n'
        f.write(buff1)
