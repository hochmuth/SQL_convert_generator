# SQL convert generator

A simple python tool for creating SQL create table/bulk insert/convert statements for SAP tables.

It parses through text files stored in one folder, reads the headers, and compares the field names against the DD03L table to determine data types. If successful, the SQL import procedure is generated as a separate file. It also creates a log file with recognized data types.

The code is written for Python 3.6.

Dependencies:
Pandas (tested on version 0.23.4)

Requirements:
- The SAP text files need to be in the form of standardized, clean data, with headers in the first row (headers need to have technical names - BUKRS, ERDAT, etc.). 
- Same encoding must be used for all text files.
- All files need to have the same extension (tested on txt and csv).
- If possible, the file name should be identical to the table name (i.e. the MKPF table should be stored in a MKPF.csv file). Joined tables are not required to follow this rule.




