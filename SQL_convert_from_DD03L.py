''' Parses through all files in a folder, extracts headers, and creates an SQL convert script.
    Prerequisites:
        Files SQL_convert_into_console.py and SQL_fields.py need to be in the same folder as the data files.
        Data files need to be in csv format.
        
    Notes:
        Separator, filetype, and encryption can be set below.        
'''
import os
import glob
import pandas as pd

# Parameters
delim = '|'
enc = 'utf_16_be'
filetype = 'csv'
path = os.path.abspath("DD03L.csv")
out_file_name = 'sql_import_all.sql'
log_file_name = 'sql_log.txt'

# SAP datatypes we want to convert
dates = ['DATS']
decimals = ['DEC', 'CURR', 'QUAN', 'FLTP']


class DataTypeSearcher:
    def __init__(self, path):
        self.path = path        
        self.field_types= pd.DataFrame()
    
    def parse_DD03L(self):
        dd03l = pd.read_csv(path, delimiter=delim, header=0, dtype=str, encoding=enc)
        self.field_types = dd03l.loc[:, ['TABNAME', 'FIELDNAME', 'DATATYPE']]
        del dd03l
        
    def get_field_type(self, table_name, field_name):
        dtype = self.field_types[(self.field_types.TABNAME == table_name) & (self.field_types.FIELDNAME == field_name)]['DATATYPE'].values[0]        
        return dtype
    

class ScriptGenerator:
    def __init__(self, file_list, out_file, log_file, separator):
        self.file_list = file_list
        self.output_file = out_file
        self.log_file = log_file
        self.separator = separator
        
    def script_beginning(self):
        self.output_file.write('USE []\nGO\nSET ANSI_NULLS ON\nGO\nSET QUOTED_IDENTIFIER ON\nGO\nCREATE PROCEDURE [dbo].[import_data]\n    @path VARCHAR(MAX)=\'\', -- Path needs to be added with a trailing backslash\n    @extension VARCHAR(4)=\''+filetype+'\'\nAS\nBEGIN\n\n')
        return self.output_file
        
    def create_tables(self):
        # Print first message.
        self.output_file.write('PRINT \'---------------------\'\n')
        self.output_file.write('PRINT \'---CREATING TABLES---\'\n')
        self.output_file.write('PRINT \'---------------------\'\n'+'\n'+'\n') 
        
        # Reads through the files and selects only headers, then divides them into column names based on selected separator
        for file in self.file_list:
            temp_file = open(file, 'r', encoding=enc)
                # Take the first line, separate into field names, remove newlines etc.
            column_names = temp_file.readline().split(self.separator)
            column_names[-1] = column_names[-1].strip()
            
            # Produce the SQL statement
            self.output_file.write('\n')
            self.output_file.write('PRINT \'[00_'+file[:-4]+']\'\n')
            self.output_file.write('IF OBJECT_ID(\'[00_'+file[:-4]+']\') IS NOT NULL DROP TABLE [00_'+file[:-4]+']\n')
            self.output_file.write('IF OBJECT_ID(\'[00_'+file[:-4]+']\') IS NULL CREATE TABLE [00_'+file[:-4]+'] (\n')
            
            
            # Main conditional. Fields.dates/fields.decimals contain the date/decimal fields to convert.
            for column in column_names:
                
                 # If it's the last column, there shouldn't be a trailing comma.
                if column == column_names[-1]:                    
                    self.output_file.write('    ['+column+'] NVARCHAR(MAX)\n')
                    self.output_file.write(')\n')
                # All other columns except the last one have the trailing comma.    
                else:
                    self.output_file.write('    ['+column+'] NVARCHAR(MAX),\n')                    

            self.output_file.write('\n'+'\n') 
        
        return self.output_file
        
    def generate_insert(self):
        # Print first message.
        self.output_file.write('PRINT \'--------------------------------\'\n')
        self.output_file.write('PRINT \'---INSERTING DATA INTO TABLES---\'\n')
        self.output_file.write('PRINT \'--------------------------------\'\n'+'\n'+'\n')
        self.output_file.write('DECLARE @InsertParam VARCHAR(MAX)\n')
        self.output_file.write('DECLARE @sql VARCHAR(MAX)\n')
        self.output_file.write('DECLARE @count VARCHAR(MAX)\n')
        self.output_file.write('SET @InsertParam = \'(FIRSTROW = 2, FIELDTERMINATOR = \'\''+self.separator+'\'\', ROWTERMINATOR = \'\'\\n\'\', CODEPAGE = \'\'ACP\'\', DATAFILETYPE = \'\'widechar\'\', TABLOCK)\'\n\n')
        
        # Reads through the files and selects only headers, then divides them into column names based on selected separator
        for file in self.file_list:
                        
            # Produce the SQL statement
            self.output_file.write('\n')
            self.output_file.write('SET @sql = \'BULK INSERT [00_'+file[:-4]+'] FROM \'\'\' + @path + \''+file[:-4]+'\' + @extension + \'\'\' WITH \' + @InsertParam; EXEC (@sql); SELECT @count = COUNT(*) FROM [00_'+file[:-4]+']; PRINT \'[00_'+file[:-4]+']: \' + @count + \' lines inserted\'')
        
        self.output_file.write('\n\n')
        return self.output_file        
                
    def generate_converts(self, DD03L):
        # Print first message.
        self.output_file.write('PRINT \'-----------------------\'\n')
        self.output_file.write('PRINT \'---CONVERTING TABLES---\'\n')
        self.output_file.write('PRINT \'-----------------------\'\n'+'\n'+'\n')

        self.log_file.write('SQL FIELD TYPES'+'\n'+'\n')        
        
        # Reads through the files and selects only headers, then divides them into column names based on selected separator
        for file in self.file_list:
            temp_file = open(file, 'r', encoding=enc)
                # Take the first line, separate into field names, remove newlines etc.
            column_names = temp_file.readline().split(self.separator)
            column_names[-1] = column_names[-1].strip()
            
            # Produce the SQL statement
            self.output_file.write('\n')
            self.output_file.write('PRINT \''+file[:-4]+'\'\n')
            self.output_file.write('IF OBJECT_ID(\'['+file[:-4]+']\') IS NOT NULL DROP TABLE ['+file[:-4]+']\n')
            self.output_file.write('SELECT\n')
            self.log_file.write(file[:-4]+':'+'\n')
            
            # Main conditional. Fields.dates/fields.decimals contain the date/decimal fields to convert.
            for column in column_names:
                
                # Get the datatype from the DD03L table                
                dtype = ''
                try:
                    dtype = DD03L.get_field_type(str(file[:-4]), str(column))
                except:
                    dtype = 'N/A'
                
                # Write the field and file type into the log file
                
                self.log_file.write('Table: '+file[:-4]+'    Field: '+column+' DType: '+dtype+'\n')
                
                # If it's the last column, there shouldn't be a trailing comma.
                if column == column_names[-1]:
                    if dtype in (dates):
                        self.output_file.write('    CASE ['+column+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+column+'], 101) END AS ['+file[:-4]+'_'+column+']\n')
                        break
                    elif dtype in (decimals):
                        self.output_file.write('    CASE WHEN CHARINDEX(\'-\', ['+column+']) > 0 THEN CONVERT(DECIMAL(15,2), SUBSTRING(['+column+'], CHARINDEX(\'-\', ['+column+']), LEN(['+column+'])) + SUBSTRING(['+column+'], 0, CHARINDEX(\'-\', ['+column+']))) ELSE CONVERT(DECIMAL(15,2), ['+column+']) END AS ['+file[:-4]+'_'+column+']\n')
                        break
                    else:
                        self.output_file.write('    LTRIM(RTRIM(['+column+'])) AS ['+file[:-4]+'_'+column+']\n')
                        break
                # All other columns except the last one have the trailing comma.    
                else:
                    if dtype in (dates):
                        self.output_file.write('    CASE ['+column+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+column+'], 101) END AS ['+file[:-4]+'_'+column+'],\n')
                    elif dtype in (decimals):
                        self.output_file.write('    CASE WHEN CHARINDEX(\'-\', ['+column+']) > 0 THEN CONVERT(DECIMAL(15,2), SUBSTRING(['+column+'], CHARINDEX(\'-\', ['+column+']), LEN(['+column+'])) + SUBSTRING(['+column+'], 0, CHARINDEX(\'-\', ['+column+']))) ELSE CONVERT(DECIMAL(15,2), ['+column+']) END AS ['+file[:-4]+'_'+column+'],\n')
                    else:
                        self.output_file.write('    LTRIM(RTRIM(['+column+'])) AS ['+file[:-4]+'_'+column+'],\n')
                        
            self.output_file.write('INTO ['+file[:-4]+']\n')
            self.output_file.write('FROM [00_'+file[:-4]+']\n')
            self.output_file.write('\n'+'\n')            
            self.log_file.write('\n'+'\n')
        return self.output_file, self.log_file
    
    def script_end(self):
        self.output_file.write('PRINT\'------------------------------------\'\n')
        self.output_file.write('PRINT\'Data import and conversions finished\'\n')
        self.output_file.write('PRINT\'------------------------------------\'\n')
        self.output_file.write('END')
        
        return self.output_file
    

def main():         
    # Open the output file
    output = open(out_file_name, 'w', encoding=enc)
    log = open(log_file_name, 'w', encoding=enc)
    
    # Read filenames from the directory you're in
    file_list = []   
    for filename in glob.glob('*.'+filetype):    
        file_list.append(filename)
    
    # Parse the DD03L for fields and data types
    Searcher = DataTypeSearcher(path)
    Searcher.parse_DD03L()
             
    # Initialize the objects
    SqlScriptGenerator = ScriptGenerator(file_list, output, log, delim)
    
    # Generate SQL script
    SqlScriptGenerator.script_beginning()
    SqlScriptGenerator.create_tables()
    SqlScriptGenerator.generate_insert()
    SqlScriptGenerator.generate_converts(Searcher)
    SqlScriptGenerator.script_end()

    # Close the output files
    output.close()
    log.close()     
    
if __name__ == "__main__":
    main()
