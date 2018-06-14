# SQL convert generator

A simple python tool for creating SQL convert statements for SAP tables.

How it works:

You place the two files ('SQL_convert_into_file.py' and 'SQL_fields.py') into the folder with the raw data and it generates an SQL convert script by parsing through the files, selecting headers, and splitting them into column names.

Files:

SQL_convert_into_file.py - main logic.

SQL_fields.py - contains two lists - dates and decimals. Each contains SAP filenames that need to be converted to date/decimal. This works, because as far as I know, the same field names always belong to the same data type, no matter what table they're in. 

