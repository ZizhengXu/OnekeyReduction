#!/usr/bin/python2
import os
import sys
os.chdir('..')
from pyraf import iraf
import re
iraf.set(stdimage='imt4096')
iraf.reset(imextn='fxf:fts,fits,fit')

f=open('llist')
l1=re.sub('\n','',f.readline())
l1=re.sub('.f','-bdf.f',l1)
print l1
f.close()

iraf.noao.imred()
iraf.noao.imred.ccdred()

outputnm=l1[:8]


f1=outputnm+'-sigclip7a-iraf.fits';os.system('rm '+f1)
iraf.noao.imred.ccdred.combine(input='@llist//-bdfa',output=f1,delete='no',combine='average',reject='sigclip',hsigma='7',lsigma='7')

f2=outputnm+'-sigclip3a-iraf.fits';os.system('rm '+f2)
iraf.noao.imred.ccdred.combine(input='@llist//-bdfa',output=f2,delete='no',combine='average',reject='sigclip',hsigma='3',lsigma='3')



os.system('ds9 '+f1+' '+f2+'&')

op=raw_input("clear up the mess?[y]/n:")
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

if not op =='n':
    santinizeOut('bd')
    santinizeOut('bdf')
    santinizeOut('bdfa')

