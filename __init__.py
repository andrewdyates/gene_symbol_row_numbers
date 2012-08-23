#!/usr/bin/python
from geo_api import *
from lab_util import *
import sys, os


def fname_is_tab(fname):
  """Is filename tab-delimited text based on file extension?"""
  return (fname.rpartition('.')[2].lower() == 'tab')
  
def load_varlist(fp):
  s = [s.partition('\t')[0].strip('\n') for s in fp]
  return s

def mean_expression_threshold(means, percentile):
  """Compute mean expression threshold above a fractional percentile."""
  threshold = np.sort(means)[int(round(np.size(means)*percentile))]
  return threshold

def gene_sym_idxs(gpl=None, means=None, threshold=None):
  """Return row numbers of unique gene symbols with maximum mean expression above percentile.

  If threshhold is None, do not use threshhold.
  """
  assert gpl is not None and means is not None
  symbols = {} # {str=>int} of gene_symbol=>row_number
  for i in xrange(len(gpl.probe_list)):
    if threshold is not None and means[i] <= threshold:
      continue
    row_id = gpl.probe_list[i]
    gene_sym = gpl.get_column(row_id, 'GENE_SYMBOL')
    if gene_sym is None:
      continue
    else:
      # Add to symbol list if new symbol or previous mean is less than this mean.
      if gene_sym not in symbols or means[symbols[gene_sym]] < means[i]:
        symbols[gene_sym] = i
  return symbols

