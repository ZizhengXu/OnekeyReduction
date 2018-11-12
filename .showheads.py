#!/usr/bin/python2
import sys
import os
os.chdir('..')
from pyraf import iraf
iraf.set(stdimage='imt4096')
iraf.reset(imextn='fxf:fts,fit')
#iraf.reset(imtype = 'fit,fts')
iraf.hselect('*.fts,*.fit','$I,CCD-TEMP,exptime,imagetyp,date-obs','yes')

