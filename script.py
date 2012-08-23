#!/usr/bin/python
"""
NOTE: This would better use the .tab GPL file definition.

python script.py outdir=$HOME/Desktop fname_brief=$HOME/Desktop/GSE7307_GPL570.gpl_brief.txt fname_data=$HOME/Desktop/GSE7307_GPL570.probes.tab
"""
nfrom geo_api import *
from lab_util import *
import sys, os

def main(outdir=None, fname_gpl_desc=None, fname_gpl_brief=None, fname_data=None):
  assert outdir and fname_gpl_desc and fname_data and fname_brief
  if not os.path.exists(outdir):
    make_dir(outdir)

  # Load GPLs
  print "Loading GPL definition from files %s and %s..." % (fname_brief, fname_gpl_desc)
  data_is_tab = (fname_data.rpartition('.')[2].lower() == 'tab')
  if data_is_tab:
    print "Loading GPL data as tab file..."
  gpl = LocalGPL(fname_brief=fname_brief, fname_data=fname_gpl_desc, data_is_tab=data_is_tab)
  gpl.load()
  print "Loaded %d row descriptions." % len(gpl.row_desc)



if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))
