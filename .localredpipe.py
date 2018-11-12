#!/usr/bin/python2
import os
os.chdir('..')
from pyraf import iraf
iraf.images()
iraf.noao()
iraf.noao.imred()
iraf.noao.imred.ccdred()
iraf.set(stdimage='imt4096')
iraf.reset(imextn='fxf:fts,fit')
iraf.reset(imtype = 'fts,fit')
from glob import glob
import astropy.io.fits as fits
import numpy as np

def makeDir(newdir):
    while(1):
        if os.path.exists(newdir):
            print "Directory %s already exists" % newdir
            return newdir
            break
        else:
            os.mkdir(newdir)
            print "New Directory '%s' created" % newdir
            return newdir
            break

def rmFile(fileroot):
    """Removes file(s) based on root name of the file
    @param fileroot: <root>*
    @type fileroot: str 
    """
    del_list = glob(fileroot+'*')
    for file in del_list:
        os.remove(file)
        print "File %s removed" % file


class Calibration:

    """
    The Calibration class contains methods to create master calibration images.
    """

    def __init__(self, caliblocation, writeto='Masters/'):
        """@param caliblocation: location of individual calibration images.
        @type caliblocation: str
        @param writeto: directory to which master calibrations are written.
                        Default is 'Masters/' created within the
                        calibdirectory.
        @type writeto: str
        """
        
        self.writedir = caliblocation + writeto
        
    def makeZero(self):
        """
        Wrapper for iraf routine zerocombine.
        Takes .fits with header imagetyp=zero and makes a master zero.
        """
        rmFile(self.writedir + 'Zero*')
        iraf.noao.imred.ccdred.zerocombine(
            input='@blist', output=self.writedir + 'Zero.fit', process='no', delete='no', clobber='no',combine='average',reject='sigclip',ccdtype='',lsigma='2',hsigma='2')
#,instrum= 'ccddb$kpno/camera.dat'
    def makeDark(self):
        """
        Wrapper for iraf routine darkcombine.
        Takes .fits with headers imagetyp=dark and makes a master dark.
        """
        rmFile(self.writedir + 'Dark*')
        iraf.noao.imred.ccdred.combine(
            input='@dlist', output=self.writedir + 'Dark.fit',rdnoise=11, delete='no',scale='none', clobber='no',ccdtype='',combine='average',reject='sigclip',lsigma='2',hsigma='2')

    def makeFlat(self):
        """
        Wrapper for iraf routine flatcombine.
        Takes .fits with headers imagetyp=flat and makes a master flat.
        """
        rmFile(self.writedir + 'Flat*')
        iraf.noao.imred.ccdred.flatcombine(
            input='@flist', output=self.writedir + 'Flat.fit', process='no', delete='no', clobber='no', subset='yes',ccdtype='',combine='median',reject='sigclip',lsigma='3',hsigma='3')

def _createMasters(reduction_dir, zero=1, dark=1, flat=1):
    """
        Calls to the calibration module to create master calibration images.
        zero, dark, and flat are set to 'yes,' but can be set to 'no' if any
        of those are not desired.
        """


    masters=Calibration(reduction_dir)
    makeDir(reduction_dir + 'Masters/')
    if zero:
        masters.makeZero()
    if dark:
        masters.makeDark()
    if flat:
        masters.makeFlat()

def santinizeOutputbdf():
    try:
        os.system('rm *-bd.f*')
        os.system('rm *-bdf.f*')
        os.system('rm *-bdfa.f*')
    except:
        pass


def reduceimg(reduction_dir):
   # reduction_dir='/mnt/hgfs/Mikesdata/wise-dec2016/U1999'
    os.chdir(reduction_dir)
    masterdir=reduction_dir + 'Masters/'
    
    _createMasters(reduction_dir)
    santinizeOutputbdf()
    
    iraf.imarith(operand1='@llist',op='-',operand2=masterdir+'Dark.fit',result='@llist//-bd')
    os.system('rm '+masterdir+'combinedFlat.fit')
    os.system('rm '+masterdir+'combinedFlatNormed.fit')
    iraf.imarith(operand1=masterdir+'Flat.fit',op='-',operand2=masterdir+'Zero.fit',result=masterdir+'combinedFlat.fit')
    med=np.mean(fits.getdata(masterdir+'combinedFlat.fit'))
    iraf.imarith(operand1=masterdir+'combinedFlat.fit',op='/',operand2=med,result=masterdir+'combinedFlatNormed.fit')
    iraf.imarith(operand1='@llist//-bd',op='/',operand2=masterdir+'combinedFlatNormed.fit',result='@llist//-bdf')
    
if "__main__"==__name__:

    reduceimg(os.getcwd())


