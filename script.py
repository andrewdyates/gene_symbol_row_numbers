#!/usr/bin/python
"""
NOTE: This would better use the .tab GPL file definition.

export STUDY_DIR=$HOME/Dropbox/biostat/study_data/GSE7307
python script.py outdir=$HOME/Desktop gpl_brief=$STUDY_DIR/GSE7307_GPL570.gpl_brief.txt gpl_data=$STUDY_DIR/GSE7307_GPL570.probes.tab
"""
from geo_api import *
from lab_util import *
import sys, os

def main(outdir=None, gpl_brief=None, gpl_data=None, data=None):
  assert outdir and gpl_brief and gpl_data
  if not os.path.exists(outdir):
    make_dir(outdir)

  # Load GPL
  print "Loading GPL definition from files %s and %s..." % (gpl_brief, gpl_data)
  data_is_tab = (gpl_data.rpartition('.')[2].lower() == 'tab')
  if data_is_tab:
    print "Loading GPL data as tab file..."
  else:
    print "Loading GPL data as SOFT text file..."
  gpl = LocalGPL(fname_brief=gpl_brief, fname_data=gpl_data, data_is_tab=data_is_tab)
  gpl.load()
  print "Loaded %d row descriptions." % len(gpl.row_desc)



if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))
