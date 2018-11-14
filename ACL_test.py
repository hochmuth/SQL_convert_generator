import pandas as pd
 
# Test table stored in a DataFrame
test_df = pd.read_csv('./Data/TEST.txt', sep='|', encoding='utf_16_le')

# DD03L table that with SAP field/table names and corresponding data types
dd03l = pd.read_csv(r'c:\temp_DATA\KraftHeinz\CCM_Monthly\Data\Converted\EU\DD03L.csv', 
                    delimiter='|', 
                    header=0, 
                    dtype=str, 
                    encoding='utf_16_be')

columns = []

print('Searching for tables')
print()

for column in test_df:
    dtype = ''    
    columns.append(column.strip())
    
    if '-' in column:
        column = column.replace('-', '_')
    
    join_split = column.split('_')
    print(join_split)
    
    # In case it's just a one word, it's probably a field name
    if len(join_split) == 1:
        print(column, 'is only one word, so it\'s probably a field name. Look at the file name for table name.')
        # Search for a data type here, once we get the file name as a variable
        print()
        continue
    
    for index, part in enumerate(join_split):
                
        try:
            table = str(dd03l[(dd03l.TABNAME == part)]['TABNAME'].values[0])
            if index == 0:
                print(part, 'is a table')
                field_name = ''
                for sub_index, subpart in enumerate(join_split[1:len(join_split)], start=1):
                    field_name += subpart                    
                    if sub_index+1 < len(join_split):
                        field_name += '_'
                print('And the field name is probably', field_name)
                # Look for the data type
                try:
                    dtype = str(dd03l[(dd03l.TABNAME == part) & (dd03l.FIELDNAME == field_name)]['DATATYPE'].values[0])
                    print('The field is of a type', dtype)
                except:
                    print('No data type found for this field')
                break
        except BaseException as e1:       
            # In case it might be V_USERNAME or other view, try adding the first two parts
            if index == 0:                
                if len(join_split) > 1:
                    part += '_'
                    part += join_split[1]
                try:
                    table = str(dd03l[(dd03l.TABNAME == part)]['TABNAME'].values[0])
                    print(part, 'is a table')
                    field_name = ''
                    for sub_index, subpart in enumerate(join_split[2:len(join_split)], start=2):
                        field_name += subpart
                        if sub_index+1 < len(join_split):
                            field_name += '_'
                    print('And the field name is probably', field_name)
                    continue
                except BaseException as e2:
                    print('Exception 2:')
                    print(e2)
                    try:
                        field = str(dd03l[(dd03l.FIELDNAME == part)]['TABNAME'].values[0])
                        print(part, 'is actually a field name')
                        break
                    except BaseException as e3:
                        print('Exception 3:')
                        print(e3)
            
            print(part, 'not found in DD03L. In other words, no idea.')
            print('Could', column, 'be a custom field name?')
            print('Exception 1:')
            print(e1)

    print()
