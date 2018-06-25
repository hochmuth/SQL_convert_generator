# SQL convert generator

A simple python tool for creating SQL convert statements for SAP tables.

How it works:

Place the two files ('SQL_convert_into_file.py' and 'SQL_fields.py') into the folder with the text files you want to import and run the  'SQL_convert_into_file.py' using Python/Anaconda/etc. It parses through the files, selecting headers, splitting them into column names, and finally generates a SQL script that you can run on the SQL server to import your data.

Note:

The resulting SQL script uses Bulk Insert that for some reason require your files to be encoded as Big Endian. For that reason I'm attaching a small PowerShell script that converts your text files to BE. (However, the Python scripts expects Unicode.)

Files:

SQL_convert_into_file.py - main logic.

SQL_fields.py - contains two lists - dates and decimals. Each contains SAP filenames that need to be converted to date/decimal. This works, because as far as I know, the same field names always belong to the same data type, no matter what table they're in. 

all_files_to_BE.ps1 - converts all files in the directory to Big Endian (see note above). Simply run it via PowerShell.

