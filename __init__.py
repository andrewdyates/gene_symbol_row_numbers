#!/usr/bin/python
from geo_api import *
from lab_util import *
import sys, os


def fname_is_tab(fname):
  """Is filename tab-delimited text based on file extension?"""
  return (fname.rpartition('.')[2].lower() == 'tab')
  
def get_gpl(gpl_brief=None, gpl_data=None, is_tab=True):
  """Return geo.GPL object from GPL file names.

  Args:
    gpl_brief: str of file path to GPL file meta data brief (as from geo_downloader)
    gpl_data: str of file path to GPL row descriptions IN DATA ROW ORDER (as from geo_downloader)
      may either be .tab for SOFT text file format
    is_tab: bool if gpl_data is in .tab format
  Returns:
    geo_api.GPL of loaded row descriptions
  """
  gpl = LocalGPL(fname_brief=gpl_brief, fname_data=gpl_data, data_is_tab=is_tab)
  gpl.load()
  return gpl

def load_varlist(fp):
  s = [s.partition('\t')[0].strip('\n') for s in fp]
  return s

def assert_row_alignment(M, varlist, gpl):
  """Assert that GPL row descriptions and row id list aligns to data rows."""
  assert np.size(M, 0) == len(gpl.row_desc) == len(gpl.probe_list) == len(gpl.probe_idx_map), \
      " != ".join((np.size(M, 0), len(gpl.row_desc), len(gpl.probe_list), len(gpl.probe_idx_map)))
  for i in xrange(np.size(M, 0)):
    s = gpl.probe_list[i]
    assert s == varlist[i]
    assert gpl.probe_idx_map[s] == i
    assert s in gpl.row_desc

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

