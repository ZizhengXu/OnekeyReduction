#!/usr/bin/python
import os
os.chdir('..')
import re




bl=open('blist','w')
dl=open('dlist','w')
fl=open('flist','w')
ll=open('llist','w')
try :
  f=open('imhead')
  for line in f:
    line=line.split()
  #  print(line)
    try:
      frtype=line[3].lower()

      if 'flat' in frtype:
        fl.write(line[0]+'\n')
      if 'bias' in frtype:
        bl.write(line[0]+'\n')
      if 'dark' in frtype:
        dl.write(line[0]+'\n')
      if 'light' in frtype:
        ll.write(line[0]+'\n')
   
    except:
      pass
  f.close()
except:
  "no imhead file"

bl.close()
dl.close()
fl.close()
ll.close()


