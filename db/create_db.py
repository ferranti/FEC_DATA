#!/usr/bin/env python
import psycopg2

#http://www.fec.gov/finance/disclosure/metadata/DataDictionaryCandidateMaster.shtml
candidate_master_sql = """CREATE TABLE candidate_master ( \
                                           ID SERIAL NOT NULL, \
                                           CAND_ID VARCHAR(14) NOT NULL, \
                                           CAND_NAME VARCHAR(250), \
                                           CAND_PTY_AFFILIATION VARCHAR(14), \
                                           CAND_ELECTION_YR SMALLINT, \
                                           CAND_OFFICE_ST VARCHAR(4), \
                                           CAND_OFFICE VARCHAR(1), \
                                           CAND_OFFICE_DISTRICT VARCHAR(4), \
                                           CAND_ICI VARCHAR(4), \
                                           CAND_STATUS VARCHAR(4), \
                                           CAND_PCC VARCHAR(14), \
                                           CAND_ST1 VARCHAR(40), \
                                           CAND_ST2 VARCHAR(40), \
                                           CAND_CITY VARCHAR(35), \
                                           CAND_ST VARCHAR(5), \
                                           CAND_ZIP VARCHAR(14));"""

#http://www.fec.gov/finance/disclosure/metadata/DataDictionaryCommitteeMaster.shtml
commitee_master_sql = """CREATE TABLE committee_master ( \
                                           ID SERIAL NOT NULL, \
                                           CMTE_ID VARCHAR(14) NOT NULL,\
                                           CMTE_NM VARCHAR(250), \
                                           TRES_NM VARCHAR(100), \
                                           CMTE_ST1 VARCHAR(40), \
                                           CMTE_ST2 VARCHAR(40), \
                                           CMTE_CITY VARCHAR(35), \
                                           CMTE_ST VARCHAR(4), \
                                           CMTE_ZIP VARCHAR(14), \
                                           CMTE_DSGN VARCHAR(4), \
                                           CMTE_TP VARCHAR(4), \
                                           CMTE_PTY_AFFILIATION VARCHAR(5), \
                                           CMTE_FILING_FREQ VARCHAR(4), \
                                           ORG_TP VARCHAR(4), \
                                           CONNECTED_ORG_NM VARCHAR(250), \
                                           CAND_ID VARCHAR(14));"""

#http://www.fec.gov/finance/disclosure/metadata/DataDictionaryCandCmteLinkage.shtml                        
candidate_linkage_sql = """CREATE TABLE candidate_linkage ( \
                                           ID SERIAL NOT NULL, \
                                           CAND_ID VARCHAR(14) NOT NULL, \
                                           CAND_ELECTION_YR SMALLINT, \
                                           FEC_ELECTION_YR SMALLINT, \
                                           CMTE_ID VARCHAR(14), \
                                           CMTE_TP VARCHAR(4), \
                                           CMTE_DSGN VARCHAR(4), \
                                           LINKAGE_ID BIGINT);"""
                                           
#http://www.fec.gov/finance/disclosure/metadata/DataDictionaryCommitteetoCommittee.shtml
comm_to_comm_sql = """CREATE TABLE comm_to_comm ( \
                                        ID SERIAL NOT NULL, \
                                        CMTE_ID VARCHAR(14), \
                                        AMNDT_IND VARCHAR(4), \
                                        RPT_TP VARCHAR(5), \
                                        TRANSACTION_PGI VARCHAR(10), \
                                        IMAGE_NUM VARCHAR(15), \
                                        TRANSACTION_TP VARCHAR(5), \
                                        ENTITY_TP VARCHAR(5), \
                                        NAME VARCHAR(250), \
                                        CITY VARCHAR(35), \
                                        STATE VARCHAR(5), \
                                        ZIP_CODE VARCHAR(14), \
                                        EMPLOYER VARCHAR(50), \
                                        OCCUPATION VARCHAR(50), \
                                        TRANSACTION_DT DATE, \
                                        TRANSACTION_AMT INTEGER, \
                                        OTHER_ID VARCHAR(14), \
                                        TRAN_ID VARCHAR(35), \
                                        FILE_NUM VARCHAR(25), \
                                        MEMO_CD VARCHAR(5), \
                                        MEMO_TEXT VARCHAR(100), \
                                        SUB_ID BIGINT UNIQUE NOT NULL);"""
                                        
# http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
cand_to_comm_sql = """CREATE TABLE cand_to_comm ( \
                                      ID SERIAL NOT NULL, \
                                      CMTE_ID VARCHAR(14) NOT NULL, \
                                      AMNDT_IND VARCHAR(5), \
                                      RPT_TP VARCHAR(5), \
                                      TRANSACTION_PGI VARCHAR(10), \
                                      IMAGE_NUM VARCHAR(15), \
                                      TRANSACTION_TP VARCHAR(5), \
                                      ENTITY_TP VARCHAR(5), \
                                      NAME VARCHAR(250), \
                                      CITY VARCHAR(35), \
                                      STATE VARCHAR(5), \
                                      ZIP_CODE VARCHAR(14), \
                                      EMPLOYER VARCHAR(50), \
                                      OCCUPATION VARCHAR(50), \
                                      TRANSACTION_DT DATE, \
                                      TRANSACTION_AMT INTEGER, \
                                      OTHER_ID VARCHAR(14), \
                                      CAND_ID VARCHAR(14), \
                                      TRAN_ID VARCHAR(35), \
                                      FILE_NUM VARCHAR(25), \
                                      MEMO_CD VARCHAR(5), \
                                      MEMO_TEXT VARCHAR(100), \
                                      SUB_ID BIGINT UNIQUE NOT NULL);"""

#http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml
individual_contrib_sql = """CREATE TABLE indiv_contrib ( \
                                          CMTE_ID VARCHAR(14) NOT NULL, \
                                          AMNDT_IND VARCHAR(5), \
                                          RPT_TP VARCHAR(5), \
                                          TRANSACTION_PGI VARCHAR(9), \
                                          IMAGE_NUM VARCHAR(15), \
                                          TRANSACTION_TP VARCHAR(5), \
                                          ENTITY_TP VARCHAR(5), \
                                          NAME VARCHAR(250), \
                                          CITY VARCHAR(35), \
                                          STATE VARCHAR(5), \
                                          ZIP_CODE VARCHAR(14), \
                                          EMPLOYER VARCHAR(50), \
                                          OCCUPATION VARCHAR(50), \
                                          TRANSACTION_DT DATE, \
                                          TRANSACTION_AMT INTEGER, \
                                          OTHER_ID VARCHAR(14), \
                                          TRAN_ID VARCHAR(35), \
                                          FILE_NUM VARCHAR(25), \
                                          MEMO_CD VARCHAR(5), \
                                          MEMO_TEXT VARCHAR(100), \
                                          SUB_ID BIGINT UNIQUE NOT NULL);"""
for i in range(2004, 2015, 2):
  conn = psycopg2.connect(dbname="FEC_%s"%i, user="postgres")
  cur = conn.cursor()
  cur.execute("""DROP TABLE IF EXISTS candidate_master;""")
  cur.execute(candidate_master_sql)
  cur.execute("""DROP TABLE IF EXISTS committee_master;""")
  cur.execute(commitee_master_sql)
  cur.execute("""DROP TABLE IF EXISTS candidate_linkage;""")
  cur.execute(candidate_linkage_sql)
  cur.execute("""DROP TABLE IF EXISTS comm_to_comm;""")
  cur.execute(comm_to_comm_sql)
  cur.execute("""DROP TABLE IF EXISTS cand_to_comm;""")
  cur.execute(cand_to_comm_sql)
  cur.execute("""DROP TABLE IF EXISTS indiv_contrib;""")
  cur.execute(individual_contrib_sql)
  conn.commit()
  

                                          