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

cnt=0;boxsize =11;bigbox = 15;maxcnt=3
while cnt<maxcnt:
    try:
        iraf.imalign(input='@llist//-bdf',reference=l1,coords='images.coord',output='@llist//-bdfa',shifts='', boxsize =boxsize,bigbox = bigbox)
    except stsci.tools.irafglobals.IrafError :
        cnt+=1
        boxsize +=10+3* cnt;bigbox += 10+3*cnt
    else: break

flag=True
if cnt>=maxcnt :
    flag=False
    f=open('autocondition','w')
    f.write('failed')
    f.close()

if flag:
    f=open('autocondition','w')
    f.write('success')
    f.close()
