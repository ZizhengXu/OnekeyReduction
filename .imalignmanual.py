#!/usr/bin/python2
import os
os.chdir('..')
import sys
from pyraf import iraf
import re
iraf.set(stdimage='imt4096')
iraf.reset(imextn='fxf:fts,fits,fit')
#iraf.reset(imtype = 'fts')
def santinizeOut(deltype):
    try:
        if 'bdfa' in deltype:
            os.system('rm *-bdfa.f*')
        else:
            if 'bdf' in deltype:
                os.system('rm *-bdf.f*')
            else:
                if 'bd' in deltype:
                    os.system('rm *-bd.f*')
    except:
        pass
    
f=open('llist')
l1=re.sub('\n','',f.readline())
l1=re.sub('.f','-bdf.f',l1)
print l1
f.close()


santinizeOut('bdfa')
import stsci.tools.irafglobals

cnt=0;boxsize =11;bigbox = 15;maxcnt=8
while cnt<maxcnt:
    try:
        iraf.imalign(input='@llist//-bdf',reference=l1,coords='images.coord',output='@llist//-bdfa',shifts='coord.shift', boxsize =boxsize,bigbox = bigbox)
    except stsci.tools.irafglobals.IrafError :
        cnt+=1
        boxsize +=10+3* cnt;bigbox += 10+3*cnt
    else: break
    
if cnt>=maxcnt :
    sys.exit(1)
"""

iraf.noao.imred()
iraf.noao.imred.ccdred()


outputnm=l1[:8]

#iraf.noao.imred.ccdred.combine(input='@llist//-bdfa',output=output,delete='yes',combine='median',reject='avsigclip')#,boxsize=22,bigbox=100
os.system('rm '+outputnm+'-avgsigclip-iraf.fits')
iraf.noao.imred.ccdred.combine(input='@llist//-bdfa',output=outputnm+'-avgsigclip-iraf.fits',delete='no',combine='median',reject='avsigclip')
os.system('rm '+outputnm+'-sigclip-iraf.fits')
iraf.noao.imred.ccdred.combine(input='@llist//-bdfa',output=outputnm+'-sigclip-iraf.fits',delete='no',combine='median',reject='sigclip')

os.system('ds9 '+outputnm+'-avgsigclip-iraf.fits '+ outputnm+'-sigclip-iraf.fits'+'&')


op=raw_input("clear up the mess?[y]/n:")
if not op =='n':
    santinizeOut('bd')
    santinizeOut('bdf')"""
