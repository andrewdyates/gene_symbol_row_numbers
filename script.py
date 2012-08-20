#!/usr/bin/python
"""
python script.py outdir=$HOME/Desktop gpl_id=GPL570
"""
from geo_api import *
from lab_util import *
import sys, os

def main(outdir=None, gpl_fname=None, gpl_id=None):
  assert outdir and gpl_id
  gpl_id = gpl_id.upper()
  if not os.path.exists(outdir):
    make_dir(outdir)

  if not gpl_fname:
    gpl_fname = os.path.join(outdir, "%s.txt" % gpl_id)
    fp = open(gpl_fname, "w")
    print "gpl_fname not provided. Downloading GPL file as %s." % (gpl_fname)
    for line in GPL.fp_download(gpl_id):
      fp.write(line)

  print "Loading GPL definition from file %s..." % (gpl_fname)
  gpl = LocalGPL(gpl_fname, gpl_id)
  gpl.load()
  print gpl
  print len(gpl.row_desc)



if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))
