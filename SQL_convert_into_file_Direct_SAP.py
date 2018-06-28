''' Parses through all files in a folder, extracts headers, and creates an SQL convert script.

    Prerequisites:
        Files SQL_convert_into_console.py and SQL_fields.py need to be in the same folder as the data files.
        Data files need to be in csv format.
        Uncoverted ('00_') tables must be already imported in the database.
        
    Notes:
        Separator and filetype can be set below.        
'''
import glob
import SQL_fields as fields

# Parameters
filetype = '.csv'
separator = '|'
out_file_name = 'sql_convert_all.sql'

class ScriptGenerator:
    def __init__(self, file_list, out_file, separator):
        self.file_list = file_list
        self.output_file = out_file
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
            temp_file = open(file, 'r', encoding='utf-16-be')
                # Take the first line, separate into field names, remove newlines etc.
            column_names = temp_file.readline().split(self.separator)
            column_names[-1] = column_names[-1].strip()
            
            # Produce the SQL statement
            self.output_file.write('\n')
            self.output_file.write('PRINT \'[00_'+file[:-4]+']\'\n')
            self.output_file.write('IF OBJECT_ID(\'[00_'+file[:-4]+']\') IS NOT NULL DROP TABLE [00_'+file[:-4]+']\n')
            self.output_file.write('IF OBJECT_ID(\'[00_'+file[:-4]+']\') IS NULL CREATE TABLE [00_'+file[:-4]+'] (\n')
            
            
            # Main conditional. Fields.dates/fields.decimals contain the date/decimal fields to convert.
            for column in column_names[1:-1]:
                column = column.strip()
                
                 # If it's the last column, there shouldn't be a trailing comma.
                if column == column_names[-2]:                    
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
            temp_file = open(file, 'r', encoding='utf-16-be')
                # Take the first line, separate into field names, remove newlines etc.
            column_names = temp_file.readline().split(self.separator)
            column_names[-1] = column_names[-1].strip()
            
            # Produce the SQL statement
            self.output_file.write('\n')
            self.output_file.write('SET @sql = \'BULK INSERT [00_'+file[:-4]+'] FROM \'\'\' + @path + \''+file[:-4]+'\' + @extension + \'\'\' WITH \' + @InsertParam; EXEC (@sql); SELECT @count = COUNT(*) FROM [00_'+file[:-4]+']; PRINT \'[00_'+file[:-4]+']: \' + @count + \' lines inserted\'')
        
        self.output_file.write('\n\n')
        return self.output_file        
                
    def generate_script(self):
        # Print first message.
        self.output_file.write('PRINT \'-----------------------\'\n')
        self.output_file.write('PRINT \'---CONVERTING TABLES---\'\n')
        self.output_file.write('PRINT \'-----------------------\'\n'+'\n'+'\n')        
        
        # Reads through the files and selects only headers, then divides them into column names based on selected separator
        for file in self.file_list:
            temp_file = open(file, 'r', encoding='utf-16-be')
                # Take the first line, separate into field names, remove newlines etc.
            column_names = temp_file.readline().split(self.separator)
            column_names[-1] = column_names[-1].strip()
            
            # Produce the SQL statement
            self.output_file.write('\n')
            self.output_file.write('PRINT \''+file[:-4]+'\'\n')
            self.output_file.write('IF OBJECT_ID(\'['+file[:-4]+']\') IS NOT NULL DROP TABLE ['+file[:-4]+']\n')
            self.output_file.write('SELECT\n')
            
            # Main conditional. Fields.dates/fields.decimals contain the date/decimal fields to convert.
            for column in column_names[1:-1]:
                column = column.strip()
                
                # If it's the last column, there shouldn't be a trailing comma.
                if column == column_names[-2]:
                    if column in (fields.dates):
                        self.output_file.write('    CASE ['+column+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+column+'], 101) END AS ['+file[:-4]+'_'+column+']\n')
                        break
                    elif column in (fields.decimals):
                        self.output_file.write('    CASE WHEN CHARINDEX(\'-\', ['+column+']) > 0 THEN CONVERT(DECIMAL(15,2), SUBSTRING(['+column+'], CHARINDEX(\'-\', ['+column+']), LEN(['+column+'])) + SUBSTRING(['+column+'], 0, CHARINDEX(\'-\', ['+column+']))) ELSE CONVERT(DECIMAL(15,2), ['+column+']) END AS ['+file[:-4]+'_'+column+']\n')
                        break
                    else:
                        self.output_file.write('    LTRIM(RTRIM(['+column+'])) AS ['+file[:-4]+'_'+column+']\n')
                        break
                # All other columns except the last one have the trailing comma.    
                else:
                    if column in (fields.dates):
                        self.output_file.write('    CASE ['+column+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+column+'], 101) END AS ['+file[:-4]+'_'+column+'],\n')
                    elif column in (fields.decimals):
                        self.output_file.write('    CASE WHEN CHARINDEX(\'-\', ['+column+']) > 0 THEN CONVERT(DECIMAL(15,2), SUBSTRING(['+column+'], CHARINDEX(\'-\', ['+column+']), LEN(['+column+'])) + SUBSTRING(['+column+'], 0, CHARINDEX(\'-\', ['+column+']))) ELSE CONVERT(DECIMAL(15,2), ['+column+']) END AS ['+file[:-4]+'_'+column+'],\n')
                    else:
                        self.output_file.write('    LTRIM(RTRIM(['+column+'])) AS ['+file[:-4]+'_'+column+'],\n')
                        
            self.output_file.write('INTO ['+file[:-4]+']\n')    
            self.output_file.write('FROM [00_'+file[:-4]+']\n')
            self.output_file.write('\n'+'\n') 
        return self.output_file
    
    def script_end(self):
        self.output_file.write('PRINT\'------------------------------------\'\n')
        self.output_file.write('PRINT\'Data import and conversions finished\'\n')
        self.output_file.write('PRINT\'------------------------------------\'\n')
        self.output_file.write('END')
        
        return self.output_file
    

def main():         
    # Open the output file
    output = open(out_file_name, 'w', encoding='utf-16-be')
    
    # Read filenames from the directory you're in
    file_list = []   
    for filename in glob.glob('*'+filetype):    
        file_list.append(filename)
          
    # Initialize the objects
    SqlScriptGenerator = ScriptGenerator(file_list, output, separator)
    
    # Generate SQL script
    SqlScriptGenerator.script_beginning()
    SqlScriptGenerator.create_tables()
    SqlScriptGenerator.generate_insert()
    SqlScriptGenerator.generate_script()
    SqlScriptGenerator.script_end()

    # Close the output file
    output.close()     
    
if __name__ == "__main__":
    main()
