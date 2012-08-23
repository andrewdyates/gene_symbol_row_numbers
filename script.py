#!/usr/bin/python
"""Get row numbers of maximum mean expression gene symbols rows with sufficient variance.

Load GPL file in row order.

EXAMPLE USE:
  export STUDY_DIR=$HOME/Dropbox/biostat/study_data/GSE7307
  python script.py outdir=$HOME/Desktop gpl_brief=$STUDY_DIR/GSE7307_GPL570.gpl_brief.txt gpl_data=$STUDY_DIR/GSE7307_GPL570.probes.tab study_data=$STUDY_DIR/GSE7307_GPL570.normed.masked.pkl varlist_fname=$STUDY_DIR/GSE7307_GPL570.varlist.txt percentile=0.25
"""
import sys, os
import cPickle as pickle
from lab_util.tab_to_npy import *
from lab_util import masked_npy_to_tab
from __init__ import *

def main(outdir=None, gpl_brief=None, gpl_data=None, study_data=None, varlist_fname=None, percentile=0.25):
  assert outdir and gpl_brief and gpl_data and study_data
  percentile = float(percentile)
  assert percentile >= 0
  if not os.path.exists(outdir):
    print "Creating output directory %s..." % (outdir)
    make_dir(outdir)

  # Load GPL.
  print "Loading GPL definition from files %s and %s..." % (gpl_brief, gpl_data)
  gpl_is_tab = fname_is_tab(gpl_data)
  if gpl_is_tab:
    print "Loading GPL data as tab file..."
  else:
    print "Loading GPL data as SOFT text file..."
  gpl = get_gpl(gpl_brief, gpl_data, gpl_is_tab)
  print "Loaded %d row descriptions." % len(gpl.row_desc)

  # Load data.
  data_is_tab = fname_is_tab(study_data)
  if data_is_tab:
    print "Loading study data file %s as tab file to numpy.MaskedArray..." % (study_data)
    M, varlist = tab_to_npy(study_data)
  else:
    assert varlist_fname, "varlist_fname parameter must be set to variable list"
    print "Loading study data file %s as pickled numpy.MaskedArray..." % (study_data)
    M = pickle.load(open(study_data))
    varlist = load_varlist(open(varlist_fname))
    assert len(varlist) == np.size(M, 0)

  print "Verifying row ID alignment between data and GPL row definitions..."
  assert_row_alignment(M=M, varlist=varlist, gpl=gpl)

  # Compute mean row (probe) expression above percentile.
  print "Computing %.2f percentile mean row expression threshold." % (percentile)
  means = M.mean(1)
  threshold = mean_expression_threshold(means, percentile)
  print "Mean expression distributions:"
  print "min: %.4f, max: %.4f, mean: %.4f, median: %.4f" % \
      (means.min(), means.max(), means.mean(), np.median(means))
  print "Minimum mean expression threshold above %.2f percentile: %.4f" % (percentile, threshold)

  # Get dictionary of gene symbols to row numbers
  d_symbols = gene_sym_idxs(gpl=gpl, means=means, threshold=threshold)
  print "Selected %d unique gene symbols" % len(d_symbols)
  idxs = sorted(d_symbols.values())

  # Output index results.
  study_id = os.path.basename(gpl_data).partition('.')[0]
  out_idx_fname = os.path.join(outdir, "%s.symbol_rownums.gt%.2f.txt" % (study_id, percentile))
  print "Saving sorted idx list in line format '[row_num]\\t[probe ID]\\t[gene symbol]\\n' to %s" \
      % (out_idx_fname)
  fp = open(out_idx_fname, "w")
  for i in idxs:
    fp.write("%d\t%s\t%s\n" % (i, varlist[i], gpl.get_column(varlist[i], 'GENE_SYMBOL')))
  fp.close()

  # Save data array copy of only selected rows.
  out_M_fname = os.path.join(outdir, "%s.gt%.2f.tab" % (os.path.basename(gpl_data), percentile))
  print "Saving %d selected rows of data matrix as .tab format as %s" % (len(idxs), out_M_fname)
  masked_npy_to_tab.npy_to_tab( \
    M[idxs, :], open(out_M_fname, 'w'), varlist=[varlist[i] for i in idxs])

  
if __name__ == "__main__":
  print sys.argv
  main(**dict([s.split('=') for s in sys.argv[1:]]))
