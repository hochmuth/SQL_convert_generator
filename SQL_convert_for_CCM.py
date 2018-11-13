''' SQL Bulk Insert/Convert Generator
    
    Parses through all files in a folder, extracts headers, checks them against the DD03L table,
    and generates an SQL bulk insert/convert script.
    
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
        DD03L -- Path to the DD03L file. Needs to include the filename.
        out_file_name -- Name of the SQL script file.
        log_file_name -- Name of the log file.
        out_file_enc -- Encoding of the output files.
    
'''
import os
import glob
import pandas as pd

# Parameters
delim = '|'
enc = 'utf_16_be'
filetype = 'csv'
data_dir = r'c:\temp_DATA\KraftHeinz\D&E\Converter\02_encoding'
DD03l_path = r'c:\temp_DATA\KraftHeinz\CCM_Monthly\Data\Converted\EU\DD03L.csv'
out_file_name = 'sql_import_files.sql'
log_file_name = 'sql_log.txt'
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
        self.field_types= pd.DataFrame()
    
    def parse_DD03L(self):
        """
        Reads the DD03L file and stores relevant fields into a Pandas DataFrame.        
        """
        
        print('Reading DD03L')
        dd03l = pd.read_csv(self.path, delimiter=delim, header=0, dtype=str, encoding=self.encoding)
        self.field_types = dd03l.loc[:, ['TABNAME', 'FIELDNAME', 'DATATYPE']]
        print('Done')
        del dd03l
        
    def get_field_type(self, table_name, field_name):
        """
        Searches the DD03L table for the data type of a SAP table/field. Returns a string with the datatype.
        
        Arguments:
        table_name -- SAP table name.
        field_name -- SAP field name.
        """
        
        dtype = self.field_types[(self.field_types.TABNAME == table_name) & (self.field_types.FIELDNAME == field_name)]['DATATYPE'].values[0]        
        return dtype
    

class ScriptGenerator:
    '''
    Main class for generating an SQL create table/bulk insert/convert script.
    Parses files in a folder, extracts the headers from the first line, separates it into field names (based on selected delimiter)
    and generates the SQL script.
    
    Arguments:
    file_list --list of files to be parsed. Needs to include whole paths, including the filenames.
    out_file -- open Python file for writing the generated SQL script.
    log_file -- open Python file for writing the generated log file.
    separator -- string containing the used delimiter.
    '''
    
    def __init__(self, file_list, out_file, log_file, separator):
        self.file_list = file_list
        self.output_file = out_file
        self.log_file = log_file
        self.separator = separator
        
    def script_beginning(self):
        '''Generates the SQL opening statements.'''
        
        self.output_file.write('USE []\nGO\nSET ANSI_NULLS ON\nGO\nSET QUOTED_IDENTIFIER ON\nGO\nCREATE PROCEDURE [dbo].[import_data]\n    @path VARCHAR(MAX)=\'\', -- Path needs to be added with a trailing backslash\n    @extension VARCHAR(4)=\'.'+filetype+'\'\nAS\nBEGIN\n\n')
        return self.output_file
        
    def create_tables(self):
        '''Generates the Create Table statements.'''
        
        print('Generating Create Table Statements')
        
        self.output_file.write('PRINT \'---------------------\'\n')
        self.output_file.write('PRINT \'---CREATING TABLES---\'\n')
        self.output_file.write('PRINT \'---------------------\'\n'+'\n'+'\n') 
        
        # Reads through the files and selects headers from the first row, 
        # then divides them into column names based on selected separator.
        for file in self.file_list:
            temp_file = open(file, 'r', encoding=enc)
            # Take the first line, separate into field name, and trim.
            column_names = temp_file.readline().split(self.separator)
            column_names[-1] = column_names[-1].strip()
            table = os.path.basename(file[:-4])
            field_name = ''
                                    
            # Produce the SQL statement
            self.output_file.write('\n')
            self.output_file.write('PRINT \'[00_'+table+']\'\n')
            self.output_file.write('IF OBJECT_ID(\'[00_'+table+']\') IS NOT NULL DROP TABLE [00_'+table+']\n')
            self.output_file.write('IF OBJECT_ID(\'[00_'+table+']\') IS NULL CREATE TABLE [00_'+table+'] (\n')
            
            
            # Go through all field names
            for column in column_names:
                field_name = column
                
                # Recognize joint tables based on '-' in the fieldname.
                if '-' in column:
                    join_split = column.split('-')
                    tab_name = join_split[0]
                    field_name = join_split[1]
                    field_name = tab_name + '_' + field_name
                
                # If it's the last column, there shouldn't be a trailing comma.
                if column == column_names[-1]:                    
                    self.output_file.write('    ['+field_name+'] NVARCHAR(255)\n')
                    self.output_file.write(')\n')
                # All other columns except the last one should have the trailing comma.    
                else:
                    self.output_file.write('    ['+field_name+'] NVARCHAR(255),\n')                    

            self.output_file.write('\n'+'\n')
            print(f'{table:50}', 'Done')        
        
        print('Create Table Statements Generated')
        return self.output_file        
        
        
    def generate_insert(self):
        '''Generates the Bulk Insert statements.'''
        
        print('Generating Insert Statements')
        
        self.output_file.write('PRINT \'--------------------------------\'\n')
        self.output_file.write('PRINT \'---INSERTING DATA INTO TABLES---\'\n')
        self.output_file.write('PRINT \'--------------------------------\'\n'+'\n'+'\n')
        self.output_file.write('DECLARE @InsertParam VARCHAR(MAX)\n')
        self.output_file.write('DECLARE @sql VARCHAR(MAX)\n')
        self.output_file.write('DECLARE @count VARCHAR(MAX)\n')
        self.output_file.write('SET @InsertParam = \'(FIRSTROW = 2, FIELDTERMINATOR = \'\''+self.separator+'\'\', ROWTERMINATOR = \'\'\\n\'\', CODEPAGE = \'\'ACP\'\', DATAFILETYPE = \'\'widechar\'\', TABLOCK)\'\n\n')
        
        # Table names are extracted from filenames:
        for file in self.file_list:
            table = os.path.basename(file[:-4])
                        
            # Produce the Bulk Insert statement
            self.output_file.write('\n')
            self.output_file.write('SET @sql = \'BULK INSERT [00_'+table+'] FROM \'\'\' + @path + \''+table+'\' + @extension + \'\'\' WITH \' + @InsertParam; EXEC (@sql); SELECT @count = COUNT(*) FROM [00_'+table+']; PRINT \'[00_'+table+']: \' + @count + \' lines inserted\'')
        
        self.output_file.write('\n\n')
        print('Done')
        return self.output_file
                
    def generate_converts(self, DD03L):
        '''
        Generate the SQL convert statements.
        Gets the right data type of each field from the DD03L table.
        
        Arguments:
        DD03L -- accepts a DataTypeSearcher object that contains a DD03L table.
        '''
        
        print('Generating Convert Table Statements')
        # Opening statements
        self.output_file.write('PRINT \'-----------------------\'\n')
        self.output_file.write('PRINT \'---CONVERTING TABLES---\'\n')
        self.output_file.write('PRINT \'-----------------------\'\n'+'\n'+'\n')

        self.log_file.write('SQL FIELD TYPES'+'\n'+'\n')     
        
        # Get field names from files
        for file in self.file_list:
            temp_file = open(file, 'r', encoding=enc)
            # Take the first line, separate into field names, and trim
            column_names = temp_file.readline().split(self.separator)
            column_names[-1] = column_names[-1].strip()
            table = os.path.basename(file[:-4])
            field_name = ''
            tab_name = table
            
            self.output_file.write('\n')
            self.output_file.write('PRINT \''+table+'\'\n')
            self.output_file.write('IF OBJECT_ID(\'['+table+']\') IS NOT NULL DROP TABLE ['+table+']\n')
            self.output_file.write('SELECT\n')
            self.log_file.write(table+':'+'\n')
            
            # Main conditional for the converts
            for column in column_names:
                field_name = column
                join_name = column
                as_name = table + '_' + column
                
                # In case it's a join table:
                if '-' in column:
                    join_split = column.split('-')
                    tab_name = join_split[0]
                    field_name = join_split[1]
                    join_name = tab_name + '_' + field_name
                    as_name = join_name
                
                # Get the datatype from the DD03L table          
                dtype = ''
                try:
                    dtype = DD03L.get_field_type(str(tab_name), str(field_name))
                except:
                    dtype = 'N/A'
                
                # Write the field and file type into the log file                
                self.log_file.write('Table: '+tab_name+'    Field: '+join_name+' DType: '+dtype+'\n')
                
                # If it's the last column, there shouldn't be a trailing comma.
                if column == column_names[-1]:
                    if dtype in (dates):
                        self.output_file.write('    CASE ['+join_name+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+join_name+'], 101) END AS ['+as_name+']\n')
                        break
                    elif dtype in (decimals):
                        self.output_file.write('    CASE WHEN CHARINDEX(\'-\', ['+join_name+']) > 0 THEN CONVERT(DECIMAL(15,2), SUBSTRING(['+join_name+'], CHARINDEX(\'-\', ['+join_name+']), LEN(['+join_name+'])) + SUBSTRING(['+join_name+'], 0, CHARINDEX(\'-\', ['+join_name+']))) ELSE CONVERT(DECIMAL(15,2), ['+join_name+']) END AS ['+as_name+']\n')
                        break
                    else:
                        self.output_file.write('    LTRIM(RTRIM(['+join_name+'])) AS ['+as_name+']\n')
                        break
                # All other columns except the last one have the trailing comma.    
                else:
                    if dtype in (dates):
                        self.output_file.write('    CASE ['+join_name+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+join_name+'], 101) END AS ['+as_name+'],\n')
                    elif dtype in (decimals):
                        self.output_file.write('    CASE WHEN CHARINDEX(\'-\', ['+join_name+']) > 0 THEN CONVERT(DECIMAL(15,2), SUBSTRING(['+join_name+'], CHARINDEX(\'-\', ['+join_name+']), LEN(['+join_name+'])) + SUBSTRING(['+join_name+'], 0, CHARINDEX(\'-\', ['+join_name+']))) ELSE CONVERT(DECIMAL(15,2), ['+join_name+']) END AS ['+as_name+'],\n')
                    else:
                        self.output_file.write('    LTRIM(RTRIM(['+join_name+'])) AS ['+as_name+'],\n')
                        
            self.output_file.write('INTO ['+table+']\n')
            self.output_file.write('FROM [00_'+table+']\n')
            self.output_file.write('\n'+'\n')            
            self.log_file.write('\n'+'\n')
            print(f'{table:50}', 'Done')
            
        print('Convert Table Statements Generated')
        return self.output_file, self.log_file
    
    def script_end(self):
        '''Generate the closing statements.'''
        print('Generating Closing Statements')
        self.output_file.write('PRINT\'------------------------------------\'\n')
        self.output_file.write('PRINT\'Data import and conversions finished\'\n')
        self.output_file.write('PRINT\'------------------------------------\'\n')
        self.output_file.write('END')
        
        print('Done')
        return self.output_file
    

def main():    
    # Open the output file
    output = open(out_file_name, 'w', encoding=out_file_enc)
    log = open(log_file_name, 'w', encoding=out_file_enc)
    
    # Read filenames from the directory you're in and store them in a list
    file_list = []
    for filename in glob.glob(data_dir+'\*.'+filetype):    
        file_list.append(filename)
        
    # Read the DD03L
    Searcher = DataTypeSearcher(path=DD03l_path, encoding=enc)
    Searcher.parse_DD03L()
             
    # Generate the SQL script
    SqlScriptGenerator = ScriptGenerator(file_list, output, log, delim)
    
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
