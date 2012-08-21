#!/usr/bin/python
"""
NOTE: This would better use the .tab GPL file definition.

python script.py outdir=$HOME/Desktop fname_brief=$HOME/Desktop/GSE7307_GPL570.gpl_brief.txt fname_data=$HOME/Desktop/GSE7307_GPL570.probes.tab
"""
from geo_api import *
from lab_util import *
import sys, os

def main(outdir=None, fname_data=None, fname_brief=None):
  assert outdir and fname_data and fname_brief
  if not os.path.exists(outdir):
    make_dir(outdir)

  print "Loading GPL definition from files %s and %s..." % (fname_brief, fname_data)
  data_is_tab = (fname_data.rpartition('.')[2].lower() == 'tab')
  gpl = LocalGPL(fname_brief=fname_brief, fname_data=fname_data, data_is_tab=data_is_tab)
  gpl.load()
  print gpl
  print gpl.attrs
  print len(gpl.row_desc)



if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))
