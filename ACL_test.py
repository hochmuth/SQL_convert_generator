import os
import glob
from datetime import datetime

import pandas as pd

delim = '|'
enc = 'utf_16_le'
filetype = 'txt'
data_dir = r'c:\temp_DATA\Python_Parser\Update_2018_10_for_ACL\Data\subpart'


dd03l_path = r'c:\temp_DATA\Python_Parser\DD03L\CEZ\DD03L.csv'
dd03l_enc = 'utf_16_be'
 


class DataTypeSearcher:
    
    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.dd03l = pd.DataFrame()
        
        # Read the DD03L table and store it inside a DataFrame
        print('Reading DD03L')
        dd03l_all = pd.read_csv(self.path, 
                                delimiter='|', 
                                header=0, 
                                dtype=str, 
                                encoding=self.encoding)
        self.dd03l = dd03l_all.loc[:, ['TABNAME', 'FIELDNAME', 'DATATYPE']]
        print('Done')
        print()
        del dd03l_all
        
    def get_field_type(self, file_name, column):
        dtype = ''
        
        if '-' in column:
            column = column.replace('-', '_')
        
        join_split = column.split('_')
        
        # In case it's just a one word, it's probably a field name
        if len(join_split) == 1:
            print(column, 'is only one word, so it\'s probably a field name. Therefore, the table name should be', file_name)
            # Search for a data type here, once we get the file name as a variable
            try:
                dtype = str(self.dd03l[(self.dd03l.TABNAME == file_name) & (self.dd03l.FIELDNAME == column)]['DATATYPE'].values[0])
                print('Found the datatype ', dtype, 'for table', file_name, 'field', column)
                print()
                return file_name, column, dtype
            except:
                print('Found nothing in DD03L for table', file_name, 'field', column)
                print('Could', column, 'be a custom field name?')
            return file_name, column, dtype
        
        for index, part in enumerate(join_split):                    
            try:
                table = str(self.dd03l[(self.dd03l.TABNAME == part)]['TABNAME'].values[0])
                if index == 0:
                    print(part, 'is a table')
                    field_name = ''
                    for sub_index, subpart in enumerate(join_split[1:len(join_split)], start=1):
                        field_name += subpart                    
                        if sub_index+1 < len(join_split):
                            field_name += '_'
                    print('And the field name is probably', field_name)
                    print('Looking for data type...')
                    # Look for the data type
                    try:
                        dtype = str(self.dd03l[(self.dd03l.TABNAME == part) & (self.dd03l.FIELDNAME == field_name)]['DATATYPE'].values[0])
                        print('The field is of a type', dtype)
                    except:
                        print('No data type found for this field')
                    return part, field_name, dtype
            except BaseException as e1:     
                # In case it might be V_USERNAME or other view, try adding the first two parts
                if index == 0:                
                    if len(join_split) > 1:
                        part += '_'
                        part += join_split[1]
                    try:
                        table = str(self.dd03l[(self.dd03l.TABNAME == part)]['TABNAME'].values[0])
                        print(table, 'is a table')
                        field_name = ''
                        for sub_index, subpart in enumerate(join_split[2:len(join_split)], start=2):
                            field_name += subpart
                            if sub_index+1 < len(join_split):
                                field_name += '_'
                        print('And the field name is probably', field_name)
                        print('Looking for data type...')
                        # Look for it's data type here
                        try:
                            dtype = str(self.dd03l[(self.dd03l.TABNAME == table) & (self.dd03l.FIELDNAME == field_name)]['DATATYPE'].values[0])
                            print('The field is of a type', dtype)
                        except:
                            print('No data type found for this field')
                        return table, field_name, dtype
                    except BaseException as e2:
                        print('Exception 2:')
                        print(e2)
                        try:
                            field = str(self.dd03l[(self.dd03l.FIELDNAME == part)]['TABNAME'].values[0])
                            print(field, 'is actually a field name')
                            break
                        except BaseException as e3:
                            print('Exception 3:')
                            print(e3)
                
                print(part, 'not found in DD03L.')
                print('Could', column, 'be a custom field name?')
                print('Exception 1:')
                print(e1)
            
        return file_name, column, dtype
    

class ScriptGenerator:
    
    def __init__(self, Searcher, file_list, out_file, log_file, separator, encoding):
        self.file_list = file_list
        self.output_file = out_file
        self.log_file = log_file
        self.separator = separator
        self.encoding = encoding
        self.Searcher = Searcher
           
        self.internal_list = []
        
    def read_the_headers(self):
        
        for file in self.file_list:
            temp_file = open(file, 'r', encoding=self.encoding)
            column_names = temp_file.readline().split(self.separator)
            table = os.path.basename(file[:-4])
            temp_list = []
            
            for column_name in column_names:
                temp_tuple = tuple()
                temp_tuple = self.Searcher.get_field_type(table, column_name.strip())
                temp_list.append(temp_tuple)
                print(temp_tuple)
                
            self.internal_list.append(temp_list)                
        
        print(self.internal_list)
        
    def script_beginning(self):
        self.output_file.write('USE []\nGO\nSET ANSI_NULLS ON\nGO\nSET QUOTED_IDENTIFIER ON\nGO\nCREATE PROCEDURE [dbo].[import_data]\n    @path VARCHAR(MAX)=\'\', -- Path needs to be added with a trailing backslash\n    @extension VARCHAR(4)=\'.'+filetype+'\'\nAS\nBEGIN\n\n')
        return self.output_file
    

    
def main():

    startTime = datetime.now()
    
    # Read filenames from a given directory you're in and store them in a list
    file_list = []
    for filename in glob.glob(data_dir+'\*.'+filetype):    
        file_list.append(filename)
    
    
    # Initialize the objects
    Searcher = DataTypeSearcher(dd03l_path, dd03l_enc)
    Generator = ScriptGenerator(Searcher, file_list, 'none', 'none', '|', enc)
    
    # Convert the headers into a table/field/dtype list 
    Generator.read_the_headers()
    
    print('Total runtime:', datetime.now() - startTime)
            
if __name__ == "__main__":
    main()
            
        
        
