''' Parses through all files in a folder, extracts headers, and creates an SQL convert script.

    Prerequisites:
        Files SQL_convert_into_console.py and SQL_fields.py need to be in the same folder as the data files.
        Data files need to be in csv format.
        Uncoverted ('00_') tables must already have been imported in the database. This is a convert script, not an import script.
        
    Notes:
        Separator and filetype can be set below.
'''
import glob
import SQL_fields as fields

filetype = '.csv'
separator = '|'

output_file = open('sql_convert_all.sql', 'w', encoding='utf-8-sig')
file_list = []

# Print first message.
output_file.write('PRINT \'---CONVERTING TABLES---\'\n')
output_file.write('PRINT \'-----------------------\'\n'+'\n'+'\n')

for filename in glob.glob('*'+filetype):    
    # TO DO: some tables have longer name. A conditional to the rescue?
    #filename = filename[-8:]
    file_list.append(filename)
    
# Reads through the files and selects only headers, then divides them into column names based on selected separator
for file in file_list:
    temp_file = open(file, 'r', encoding='utf-8-sig')
        # Take the first line, separate into field names, remove newlines etc.
    column_names = temp_file.readline().split(separator)
    column_names[-1] = column_names[-1].strip()
    
    # Produce the SQL statement
    output_file.write('\n')
    output_file.write('PRINT \''+file[:-4]+'\'\n')
    output_file.write('IF OBJECT_ID(\'['+file[:-4]+']\') IS NOT NULL DROP TABLE ['+file[:-4]+']\n')
    output_file.write('SELECT\n')
    
    # Main conditional. Fields.dates/fields.decimals contain the date/decimal fields to convert.
    for column in column_names:
        
        # If it's the last column, there shouldn't be a trailing comma.
        if column == column_names[-1]:
            if column in (fields.dates):
                output_file.write('CASE ['+column+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+column+'], 101) END AS ['+file[:-4]+'_'+column+']\n')
                break
            elif column in (fields.decimals):
                output_file.write('CASE WHEN CHARINDEX(\'-\', ['+column+']) > 0 THEN CONVERT(DECIMAL(15,2), SUBSTRING(['+column+'], CHARINDEX(\'-\', ['+column+']), LEN(['+column+'])) + SUBSTRING(['+column+'], 0, CHARINDEX(\'-\', ['+column+']))) ELSE CONVERT(DECIMAL(15,2), ['+column+']) END AS ['+file[:-4]+'_'+column+']\n')
                break
            else:
                output_file.write('LTRIM(RTRIM(['+column+'])) AS ['+file[:-4]+'_'+column+']\n')
                break
        # All other columns except the last one have the trailing comma.    
        else:
            if column in (fields.dates):
                output_file.write('CASE ['+column+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+column+'], 101) END AS ['+file[:-4]+'_'+column+'],\n')
            elif column in (fields.decimals):
                output_file.write('CASE WHEN CHARINDEX(\'-\', ['+column+']) > 0 THEN CONVERT(DECIMAL(15,2), SUBSTRING(['+column+'], CHARINDEX(\'-\', ['+column+']), LEN(['+column+'])) + SUBSTRING(['+column+'], 0, CHARINDEX(\'-\', ['+column+']))) ELSE CONVERT(DECIMAL(15,2), ['+column+']) END AS ['+file[:-4]+'_'+column+'],\n')
            else:
                output_file.write('LTRIM(RTRIM(['+column+'])) AS ['+file[:-4]+'_'+column+'],\n')
                
    output_file.write('INTO ['+file[:-4]+']\n')    
    output_file.write('FROM [00_'+file[:-4]+']\n')
    output_file.write('\n'+'\n')
    
    # Close the file
    temp_file.close()

# Close the output file
output_file.close()     
        

