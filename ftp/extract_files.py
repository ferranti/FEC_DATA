#!/usr/bin/env python
import zipfile
import os
import config

files = {"data/%s/cm%s.zip"    : "data/%s/cm%s/",    # Committee Master File
         "data/%s/cn%s.zip"    : "data/%s/cn%s/",    # Candidate Master File
	 "data/%s/cn%s.zip"    : "data/%s/cn%s/",    # Candidate Committee Linkage File
	 "data/%s/oth%s.zip"   : "data/%s/oth%s/",   # Any transaction from one committee to another
	 "data/%s/pas2%s.zip"  : "data/%s/pas2%s/",  # Contributions to candidates (and other expenditures) from committees
	 "data/%s/indiv%s.zip" : "data/%s/indiv%s/", # Contributions by individuals
	}

for year in range(config.start_year, 2015, 2):
  year_suffix = str(year)[2:]
  for f in files:
    archive = f % (year, year_suffix)
    extract_to = files[f] % (year, year_suffix)
    if not os.path.isdir(extract_to):
      os.mkdir(extract_to)
    zf = zipfile.ZipFile(archive)
    print "Extracting %s to %s" % (archive, extract_to)
    