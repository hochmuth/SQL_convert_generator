''' SQL Bulk Insert/Convert Generator
    
    Parses through all files in a folder, extracts headers, checks them against the DD03L table,
    and generates an SQL bulk insert/convert script.
    Works for files downloaded through SmartExporter and ACL.
    
    Dependencies:
        Pandas (tested on version 0.23.4)
    
    Prerequisites:
        Data files need to be in the same format (txt or csv) and need to have the same encoding. Filenames need to 
        be same as table names.
        Fieldnames have to be in the first row.   
        For generating the convert statements, you also need a DD03L table with technical names in the header.
        
    Parameters:
        delim -- Delimiter used in the files.
        enc -- Encoding of the files.
        filetype -- Filetype of the text files.
        data_dir -- Path to text files (needs to be written WITHOUT the trailing backslash).
        
        dd03l_path -- Path to the DD03L file. Needs to include the filename.
        dd03l_enc -- Encoding of the DD03L file.
        out_file_name -- Name of the SQL script file.
        log_file_name -- Name of the log file.
        out_file_enc -- Encoding of the output files.
    
'''

import os
import glob
from datetime import datetime

import pandas as pd

# PARAMETERS
# Text files
delim = '|'
enc = 'utf-16'
filetype = 'csv'
data_dir = r''

# DD03L
dd03l_path = r''
dd03l_enc = 'utf_16_be'

# Output files
out_file_name = 'sql_import_files.sql'
log_file_name = 'sql_log.log'
out_file_enc = 'utf_8'

# SAP datatypes we want to convert
dates = ['DATS']
decimals = ['DEC', 'CURR', 'QUAN', 'FLTP']

class DataTypeSearcher:
    ''' 
    Determines the datatype of SAP fields by comparing field names to the DD03L table.
    The table is stored in a Pandas DataFrame.
    
    Arguments:
    path -- location of the DD03L table on disk. Needs to include the filename.
    encoding -- encoding of the DD03L file. 
    '''
    
    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.dd03l = pd.DataFrame()
        self.dd03l_all = pd.DataFrame()
        
        # Read the DD03L table and store it inside a DataFrame
        print('Reading DD03L')
        try:
            dd03l_all = pd.read_csv(self.path, 
                                    delimiter='|', 
                                    header=0, 
                                    dtype=str, 
                                    encoding=self.encoding)
            self.dd03l = dd03l_all.loc[:, ['TABNAME', 'FIELDNAME', 'DATATYPE']]
            print('Done')
        except:            
            raise RuntimeError('Problem reading DD03L')
            
        del dd03l_all    
        # List containing all table names from DD03L
        self.all_tables = self.dd03l.TABNAME.unique().tolist()        
        print()
        
    def get_field_type(self, file_name, column):
        ''' 
        Arguments:
            file_name -- text file name
            column -- column from the header
        Returns a tuple containing:
            file name -- to keep track of it in each tuple (needed for SQL statements)
            table name -- based on file name or field name
            field name
            data type -- if found in DD03L
        '''
        dtype = ''
        
        # SmartExporter tables use hyphen instead of underscore
        if '-' in column:
            column = column.replace('-', '_')
        
        join_split = column.split('_')
        
        # In case it's just a one word, assume it's a field name
        if len(join_split) == 1:
            try:
                dtype = str(self.dd03l[(self.dd03l.TABNAME == file_name) & (self.dd03l.FIELDNAME == column)]['DATATYPE'].values[0])
                return file_name, file_name, column, dtype
            except:
                return file_name, file_name, column, dtype
        
        # If it's more than one word, look into DD03L for the first word in DD03L
        for index, part in enumerate(join_split):                    
            if part in self.all_tables:
                table = part
                # If the first word is a table, the rest is probably the field name
                if index == 0:
                    field_name = ''
                    for sub_index, subpart in enumerate(join_split[1:len(join_split)], start=1):
                        field_name += subpart                    
                        if sub_index+1 < len(join_split):
                            field_name += '_'
                    # Assuming the rest is a field name, look for its data type
                    try:
                        dtype = str(self.dd03l[(self.dd03l.TABNAME == part) & (self.dd03l.FIELDNAME == field_name)]['DATATYPE'].values[0])
                    except:
                        pass
                    # Return the full tuple, even if data type not found
                    return file_name, part, field_name, dtype
            # If the first word doesn't return any match in DD03L
            else:     
                # In case it might be V_USERNAME or other view, try adding the first two parts and look for that
                if index == 0:                
                    if len(join_split) > 1:
                        part += '_'
                        part += join_split[1]
                    if part in self.all_tables:
                        table = part
                        field_name = ''
                        for sub_index, subpart in enumerate(join_split[2:len(join_split)], start=2):
                            field_name += subpart
                            if sub_index+1 < len(join_split):
                                field_name += '_'
                        # Look for its data type here
                        try:
                            dtype = str(self.dd03l[(self.dd03l.TABNAME == table) & (self.dd03l.FIELDNAME == field_name)]['DATATYPE'].values[0])
                        except:
                            pass
                            # Return the tuple in any case
                        return file_name, table, field_name, dtype
                    # If no match is found for the first two parts, stop searching and take the whole thing for a field name
                    else:
                        break
        
        # In case the search fails, return everything 
        return file_name, file_name, column, dtype
    

class ScriptGenerator:
    '''
    Main class for generating an SQL create table/bulk insert/convert script.
    Parses files in a folder, extracts the headers from the first line, separates it into field names (based on selected delimiter).
    For each file and field it subsequently calls DataTypeSearcher.get_field_type() method.
    Results are stored in internal_list.
    
    Arguments:
    Searcher -- has to be an object of DataTypeSearcher class.
    file_list --list of files to be parsed. Needs to include whole paths, including the filenames.
    out_file -- open Python file for writing the generated SQL script.
    log_file -- open Python file for writing the generated log file.
    separator -- string containing the used delimiter.
    encoding -- text files encoding.
    '''
    
    def __init__(self, Searcher, file_list, out_file, log_file, separator, encoding):
        self.Searcher = Searcher
        self.file_list = file_list
        self.output_file = out_file
        self.log_file = log_file
        self.separator = separator
        self.encoding = encoding        
        
        # List for storing the data type tuples
        self.internal_list = []
        
    def read_the_headers(self):
        '''
        Reads the header of each file and tries to get the right table name, field name, and data type from the DD03L table.
        It stores the result (tuple of the lenght of 4) in the internal list to make the remaining methods run much faster
        (no need to parse DD03L every time).
        '''
        
        print('Parsing the files')
        
        # Open each file and read the header
        for file in self.file_list:
            temp_file = open(file, 'r', encoding=self.encoding)
            column_names = temp_file.readline().split(self.separator)
            table = os.path.basename(file[:-4])
            temp_list = []
                        
            # Divide the headers based on selected delimiter and search for data types
            for column_name in column_names:
                temp_tuple = tuple()
                temp_tuple = self.Searcher.get_field_type(table, column_name.strip())
                temp_list.append(temp_tuple)
                        
            print(file, 'parsed')
            self.internal_list.append(temp_list)  
        
        print('Done')
        print()
        return
    
    def print_internal_list(self):
        ''' Prints the internal list for debugging purposes. '''
        
        for table_list in self.internal_list:
            for field_list in table_list:
                print('File:', field_list[0], 'Table:', field_list[1], 'Field:', field_list[2], 'Data Type:', field_list[3])
        
        print()
        return
    
    # Script creation methods
    def script_beginning(self):
        '''Generates the SQL opening statements.'''
        
        self.output_file.write('USE []\nGO\nSET ANSI_NULLS ON\nGO\nSET QUOTED_IDENTIFIER ON\nGO\nCREATE PROCEDURE [dbo].[import_data]\n    @path VARCHAR(MAX)=\'\', -- Path needs to be added with a trailing backslash\n    @extension VARCHAR(4)=\'.'+filetype+'\'\nAS\nBEGIN\n\n')
        return
    
    def create_table(self):
        '''Generates the Create Table statements.'''
        
        print('Generating Create Table Statements')
        
        # SQL 
        self.output_file.write('PRINT \'---------------------\'\n')
        self.output_file.write('PRINT \'---CREATING TABLES---\'\n')
        self.output_file.write('PRINT \'---------------------\'\n'+'\n'+'\n') 
        
        # For all files
        for table_list in self.internal_list:
            fin_table = table_list[0][0]
            last_field = table_list[-1][1] + '_' + table_list[-1][2]
            
            # SQL
            self.output_file.write('\n')
            self.output_file.write('PRINT \'[00_'+fin_table+']\'\n')
            self.output_file.write('IF OBJECT_ID(\'[00_'+fin_table+']\') IS NOT NULL DROP TABLE [00_'+fin_table+']\n')
            self.output_file.write('IF OBJECT_ID(\'[00_'+fin_table+']\') IS NULL CREATE TABLE [00_'+fin_table+'] (\n')
            
            # Go through the fields       
            for field_list in table_list:
                fin_field = field_list[1] + '_' + field_list[2]
                
                # If it's the last column, there shouldn't be a trailing comma.
                if fin_field == last_field:
                    self.output_file.write('    ['+fin_field+'] NVARCHAR(255)\n')
                    self.output_file.write(')\n')
                # All columns except the last one should have the trailing comma.    
                else: 
                    self.output_file.write('    ['+fin_field+'] NVARCHAR(255),\n')
            
            self.output_file.write('\n'+'\n')
            print(f'{table_list[0][0]:50}', 'Done')  
        
        print('Create Table Statements Generated')
        print()
        return
    
    def bulk_insert(self):
        '''Generates the Bulk Insert statements.'''
        
        print('Generating Insert Statements')
        
        self.output_file.write('PRINT \'--------------------------------\'\n')
        self.output_file.write('PRINT \'---INSERTING DATA INTO TABLES---\'\n')
        self.output_file.write('PRINT \'--------------------------------\'\n'+'\n'+'\n')
        self.output_file.write('DECLARE @InsertParam VARCHAR(MAX)\n')
        self.output_file.write('DECLARE @sql VARCHAR(MAX)\n')
        self.output_file.write('DECLARE @count VARCHAR(MAX)\n')
        self.output_file.write('SET @InsertParam = \'(FIRSTROW = 2, FIELDTERMINATOR = \'\''+self.separator+'\'\', ROWTERMINATOR = \'\'\\n\'\', CODEPAGE = \'\'ACP\'\', DATAFILETYPE = \'\'widechar\'\', TABLOCK)\'\n\n')
        
        # For all files
        for table_list in self.internal_list:
            fin_table = table_list[0][0]
            
            self.output_file.write('\n')
            self.output_file.write('SET @sql = \'BULK INSERT [00_'+fin_table+'] FROM \'\'\' + @path + \''+fin_table+'\' + @extension + \'\'\' WITH \' + @InsertParam; EXEC (@sql); SELECT @count = COUNT(*) FROM [00_'+fin_table+']; PRINT \'[00_'+fin_table+']: \' + @count + \' lines inserted\'')
        
        self.output_file.write('\n\n')
        
        print('Done')
        print()
        return
    
    def convert_table(self):
        '''Generates the Bulk Insert statements.'''
        
        print('Generating Convert Table Statements')
        
         # Opening statements
        self.output_file.write('PRINT \'-----------------------\'\n')
        self.output_file.write('PRINT \'---CONVERTING TABLES---\'\n')
        self.output_file.write('PRINT \'-----------------------\'\n'+'\n'+'\n')

        self.log_file.write('SQL FIELD TYPES'+'\n'+'\n')  
        
        # For all files
        for table_list in self.internal_list:
            fin_table = table_list[0][0]
            last_field = table_list[-1][1] + '_' + table_list[-1][2]
            
            self.output_file.write('\n')
            self.output_file.write('PRINT \''+fin_table+'\'\n')
            self.output_file.write('IF OBJECT_ID(\'['+fin_table+']\') IS NOT NULL DROP TABLE ['+fin_table+']\n')
            self.output_file.write('SELECT\n')
            self.log_file.write(fin_table+':'+'\n')
            
            # For all fields in a file
            for field_list in table_list:
                fin_field = field_list[1] + '_' + field_list[2]
                fin_dtype = field_list[3]
                as_field = field_list[1] + '_' + fin_field
                
                self.log_file.write('Table: '+fin_table+'    Field: '+as_field+' DType: '+fin_dtype+'\n')
                
                # If it's the last column, there shouldn't be a trailing comma.
                if fin_field == last_field:
                    if fin_dtype in (dates):
                        self.output_file.write('    CASE ['+fin_field+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+fin_field+'], 101) END AS ['+fin_field+']\n')
                        break
                    elif fin_dtype in (decimals):
                        self.output_file.write('    CASE WHEN CHARINDEX(\'-\', ['+fin_field+']) > 0 THEN CONVERT(DECIMAL(16,3), SUBSTRING(['+fin_field+'], CHARINDEX(\'-\', ['+fin_field+']), LEN(['+fin_field+'])) + SUBSTRING(['+fin_field+'], 0, CHARINDEX(\'-\', ['+fin_field+']))) ELSE CONVERT(DECIMAL(16,3), ['+fin_field+']) END AS ['+fin_field+']\n')
                        break
                    else:
                        self.output_file.write('    LTRIM(RTRIM(['+fin_field+'])) AS ['+fin_field+']\n')
                        break
                # All columns except the last one have the trailing comma.
                else:
                    if fin_dtype in (dates):
                        self.output_file.write('    CASE ['+fin_field+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+fin_field+'], 101) END AS ['+fin_field+'],\n')
                    elif fin_dtype in (decimals):
                        self.output_file.write('    CASE WHEN CHARINDEX(\'-\', ['+fin_field+']) > 0 THEN CONVERT(DECIMAL(16,3), SUBSTRING(['+fin_field+'], CHARINDEX(\'-\', ['+fin_field+']), LEN(['+fin_field+'])) + SUBSTRING(['+fin_field+'], 0, CHARINDEX(\'-\', ['+fin_field+']))) ELSE CONVERT(DECIMAL(16,3), ['+fin_field+']) END AS ['+fin_field+'],\n')
                    else:
                        self.output_file.write('    LTRIM(RTRIM(['+fin_field+'])) AS ['+fin_field+'],\n')
            
            self.output_file.write('INTO ['+fin_table+']\n')
            self.output_file.write('FROM [00_'+fin_table+']\n')
            self.output_file.write('\n'+'\n')            
            self.log_file.write('\n'+'\n')
            print(f'{fin_table:50}', 'Done')
            
        print('Convert Table Statements Generated')
        print()
        return
    
    def script_end(self):
        '''Generate the closing statements.'''
        
        print('Generating Closing Statements')
        self.output_file.write('PRINT\'------------------------------------\'\n')
        self.output_file.write('PRINT\'Data import and conversions finished\'\n')
        self.output_file.write('PRINT\'------------------------------------\'\n')
        self.output_file.write('END')
        
        print('Done')
        print()
        return
            
def main():
    
    # Keep track of time
    startTime = datetime.now()
    
    # Open the output files
    output = open(out_file_name, 'w', encoding=out_file_enc)
    log = open(log_file_name, 'w', encoding=out_file_enc)
    
    # Read filenames from a given directory you're in and store them in a list
    file_list = []
    for filename in glob.glob(data_dir+'\*.'+filetype):    
        file_list.append(filename)    
    
    # Initialize the objects
    Searcher = DataTypeSearcher(dd03l_path, dd03l_enc)
    Generator = ScriptGenerator(Searcher, file_list, output, log, '|', enc)
    
    # Prepare the data 
    Generator.read_the_headers()
    #Generator.print_internal_list()
    
    # Generate the script
    Generator.script_beginning()
    Generator.create_table()
    Generator.bulk_insert()
    Generator.convert_table()
    Generator.script_end()
    
    print('Total runtime:', datetime.now() - startTime)
    
    # Clean-up
    del Searcher
    del Generator
    
    # Close the output files
    output.close()
    log.close()
            
if __name__ == "__main__":
    main()
    
