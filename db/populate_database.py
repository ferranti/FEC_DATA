#!/usr/bin/env python

import psycopg2
import os
from datetime import datetime

def read_some_lines(file_object, chunk_size=1024):
  while True:
    data = file_object.readlines(chunk_size)
    if not data:
      break
    yield data

def populate_database(start_year, end_year, cwd, Connection):
  """Populates FEC databases based on parameters listed in the config.py file in the root of this package"""
    
  files = {"committee_master_%s"  : ["%s/data/%s/cm%s/cm.txt", "%s/db/headers/cm_header_file.csv"],
           "candidate_master_%s"  : ["%s/data/%s/cn%s/cn.txt", "%s/db/headers/cn_header_file.csv"],
           "candidate_linkage_%s" : ["%s/data/%s/ccl%s/ccl.txt", "%s/db/headers/ccl_header_file.csv"],
           "comm_to_comm_%s"      : ["%s/data/%s/oth%s/itoth.txt","%s/db/headers/oth_header_file.csv"],
           "cand_to_comm_%s"      : ["%s/data/%s/pas2%s/itpas2.txt", "%s/db/headers/pas2_header_file.csv"],
           "indiv_contrib_%s"     : ["%s/data/%s/indiv%s/itcont.txt", "%s/db/headers/indiv_header_file.csv"]
           }

  files_1998 = {"committee_master_%s"  : ["%s/data/%s/cm%s/cm.txt", "%s/db/headers/cm_header_file.csv"],
                "candidate_master_%s"  : ["%s/data/%s/cn%s/cn.txt", "%s/db/headers/cn_header_file.csv"],
                "comm_to_comm_%s"      : ["%s/data/%s/oth%s/itoth.txt","%s/db/headers/oth_header_file.csv"],
                "cand_to_comm_%s"      : ["%s/data/%s/pas2%s/itpas2.txt", "%s/db/headers/pas2_header_file.csv"],
                "indiv_contrib_%s"     : ["%s/data/%s/indiv%s/itcont.txt", "%s/db/headers/indiv_header_file.csv"]
                }

  if not os.path.isdir("%s/db/errors" % cwd):
    os.mkdir("%s/db/errors" % cwd)
  
  errors = open("%s/db/errors/errors.txt" % cwd, "wb")
  for year in range(start_year, end_year, 2):
    year_suffix = str(year)[2:]
      
    if year <= 1998:
      tempfiles = files_1998
    else:
      tempfiles = files
      
    for table in sorted(tempfiles):
      f = table % year
      print "CURRENT YEAR: %s\nCURRENT TABLE: %s" % (year, f)
      try:
        temp = open(files[table][0] % (cwd, year, year_suffix))
        template = open(files[table][1] % cwd).read().strip()
      except IOError:
	print "Have you run 'make download && make extract yet'?"
	os.sys.exit(1)
      template = str(tuple(template.split(","))).replace("'", "").lower()
      for chunk in read_some_lines(temp):
        for line in chunk:
	  temp1 = line.replace("\x92", "")
	  temp1 = temp1.replace("\xa0", " ")
	  temp1 = temp1.replace("\x85", "...")
	  temp1 = temp1.strip().replace("'", "").split("|")
	  if f in ("comm_to_comm_%s" % year, "cand_to_comm_%s" % year, "indiv_contrib_%s" % year):
	    if temp1[13]:
	      date = temp1[13]
	      try:
	        date = datetime(month=int(date[0:2]), day=int(date[2:4]), year=int(date[4:]))
	      except ValueError as e:
		print "Error: %s %s\nContinuing" % (e, temp1[13])
		to_write = "%s|%s\n" % (year, str(temp1))
		errors.write(to_write)
		errors.flush()
		continue
	      temp1[13] = date.strftime("%Y%m%d")
	    else:
	      date = datetime(month=01, day=01, year=1900)
	      temp1[13] = date.strftime("%Y%m%d")	   
	  temp1 = tuple(temp1)
	  try:
	    query = "INSERT INTO %s %s VALUES %s;" % (f, template, temp1)
	    Connection.cur.execute("BEGIN;")
	    Connection.cur.execute("SAVEPOINT save_point;")
            Connection.cur.execute(query)
          except (psycopg2.DataError, psycopg2.InternalError) as e:
            print "Error: %s %s\nContinuing" % (e, temp1[13])
            to_write = "%s|%s\n" % (year, str(temp1))
	    errors.write(to_write)
	    errors.flush()
	    Connection.cur.execute("ROLLBACK TO SAVEPOINT save_point;")
	    continue
	  except psycopg2.IntegrityError as e:
	    print "Failed to integrate due to constraints %s" % query
	    print "Database already populated! Exiting NOW!"
	    Connection.cur.execute("ROLLBACK TO SAVEPOINT save_point;")
	    continue
	  else:
	    Connection.cur.execute("COMMIT;")
	    #os.sys.exit(1)
      Connection.conn.commit()
      
  Connection.conn.close()
