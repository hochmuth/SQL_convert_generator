# Parses through the folder and lists all the files.
import glob
import fields

file_list = []

for filename in glob.glob('*.csv'):    
    # TO DO: some tables have longer name. A conditional to the rescue?
    #filename = filename[-8:]
    file_list.append(filename)
    
# Reads through the files and selects only headers, then divides them into column names based on selected separator
for file in file_list:
    temp_file = open(file, 'r', encoding='utf-8-sig')
        # Take the first line, separate into field names, remove newlines etc.
    column_names = temp_file.readline().split('|')
    column_names[-1] = column_names[-1].strip()
    
    # Produce the SQL statement
    print('PRINT \''+file[:-4]+'\'')
    print('SELECT')
    
    # Main conditional. Fields.dates/fields.decimals contain the date/decimal fields to convert.
    for column in column_names:
        
        # If it's the last column, there shouldn't be a trailing comma.
        if column == column_names[-1]:
            if column in (fields.dates):
                print('CASE ['+column+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+column+'], 101) END AS ['+file[:-4]+'_'+column+']')
                break
            elif column in (fields.decimals):
                print('CASE WHEN CHARINDEX(\'-\', ['+column+']) > 0 THEN CONVERT(DECIMAL(15,2), SUBSTRING(['+column+'], CHARINDEX(\'-\', ['+column+']), LEN('+column+')) + SUBSTRING(['+column+'], 0, CHARINDEX(\'-\', ['+column+']))) ELSE CONVERT(DECIMAL(15,2), ['+column+']) END AS ['+file[:-4]+'_'+column+']')
                break
            else:
                print('LTRIM(RTRIM(['+column+'])) AS ['+file[:-4]+'_'+column+']')
                break
        # All other columns except the last one:    
        else:
            if column in (fields.dates):
                print('CASE ['+column+'] WHEN \'00000000\' THEN NULL ELSE CONVERT(DATE, ['+column+'], 101) END AS ['+file[:-4]+'_'+column+'],')
            elif column in (fields.decimals):
                print('CASE WHEN CHARINDEX(\'-\', ['+column+']) > 0 THEN CONVERT(DECIMAL(15,2), SUBSTRING(['+column+'], CHARINDEX(\'-\', ['+column+']), LEN('+column+')) + SUBSTRING(['+column+'], 0, CHARINDEX(\'-\', ['+column+']))) ELSE CONVERT(DECIMAL(15,2), ['+column+']) END AS ['+file[:-4]+'_'+column+'],')
            else:
                print('LTRIM(RTRIM(['+column+'])) AS ['+file[:-4]+'_'+column+'],')
                
    print('INTO ['+file[:-4]+']')    
    print('FROM [00_'+file[:-4]+']')
    print('\n')
    
    # Close the file, dude. Good manners, is all.
    temp_file.close()
        
        # TO DO:
        # Check different separators.
        
        
        
        
