#!/usr/bin/python
"""Get row numbers of maximum mean expression gene symbols rows with sufficient variance.

Load GPL file in row order.

EXAMPLE USE:
  export STUDY_DIR=$HOME/Dropbox/biostat/study_data/GSE7307
  python script.py outdir=$HOME/Desktop gpl_brief=$STUDY_DIR/GSE7307_GPL570.gpl_brief.txt gpl_data=$STUDY_DIR/GSE7307_GPL570.probes.tab study_data=$STUDY_DIR/GSE7307_GPL570.normed.masked.pkl varlist_fname=$STUDY_DIR/GSE7307_GPL570.varlist.txt
"""
from geo_api import *
from lab_util import *
import cPickle as pickle
from lab_util.tab_to_npy import *
import sys, os

def main(outdir=None, gpl_brief=None, gpl_data=None, study_data=None, varlist_fname=None):
  assert outdir and gpl_brief and gpl_data and study_data
  if not os.path.exists(outdir):
    make_dir(outdir)

  # Load GPL.
  print "Loading GPL definition from files %s and %s..." % (gpl_brief, gpl_data)
  data_is_tab = (gpl_data.rpartition('.')[2].lower() == 'tab')
  if data_is_tab:
    print "Loading GPL data as tab file..."
  else:
    print "Loading GPL data as SOFT text file..."
  gpl = LocalGPL(fname_brief=gpl_brief, fname_data=gpl_data, data_is_tab=data_is_tab)
  gpl.load()
  print "Loaded %d row descriptions." % len(gpl.row_desc)

  # Load Data.
  data_is_tab = (study_data.rpartition('.')[2].lower() == 'tab')
  if data_is_tab:
    print "Loading study data file %s as tab file to numpy.MaskedArray..." % (study_data)
    M, varlist = tab_to_npy(tab_fname)
  else:
    assert varlist_fname, "varlist_fname parameter must be set to variable list"
    print "Loading study data file %s as pickled numpy.MaskedArray..." % (study_data)
    M = pickle.load(open(study_data))
    varlist = [s.partition('\t')[0].strip('\n') for s in open(varlist_fname)]
    assert len(varlist) == np.size(M, 0)

  # Assert that GPL row descriptions and row id list aligns to data rows.
  print "Verifying row ID alignment..."
  print np.size(M, 0), len(gpl.row_desc), len(gpl.probe_list), len(gpl.probe_idx_map)
  assert np.size(M, 0) == len(gpl.row_desc) == len(gpl.probe_list) == len(gpl.probe_idx_map)
  for i in xrange(np.size(M, 0)):
    s = gpl.probe_list[i]
    assert s == varlist[i]
    assert gpl.probe_idx_map[s] == i
    assert s in gpl.row_desc
  print "Row alignment verified."


if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))
