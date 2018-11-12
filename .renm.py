#!/usr/bin/python
import os
import re
os.chdir('..')
l=os.listdir('.')
for file in l:
  if '@' in file:
    os.rename(file,re.sub('@','at',file))
  if '.FTS' in file:
    os.rename(file,re.sub('.FTS','.fit',file))
  if ' ' in file:
    os.rename(file,re.sub(' ','_',file))
def santinizeOutputbdf():
    try:
        os.system('rm *-bd.f*')
        os.system('rm *-bdf.f*')
        os.system('rm *-bdfa.f*')
    except:
        pass
santinizeOutputbdf()
