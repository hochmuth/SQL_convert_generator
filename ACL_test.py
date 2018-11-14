import pandas as pd
 
# Test table stored in a DataFrame
test_df = pd.read_csv('./Data/BSIK_BSAK_BKPF.txt', sep='|', encoding='utf_16_le')

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
    columns.append(column.strip())
    
    join_split = column.split('_')
    print(join_split)
    
    for index, part in enumerate(join_split):
        dtype = ''
        
        try:
            table = str(dd03l[(dd03l.TABNAME == part)]['TABNAME'].values[0])
            if index == 0:
                print(part, 'is a table')
                field_name = ''
                for sub_index, subpart in enumerate(join_split[1:len(join_split)], start=1):
                    field_name += subpart                    
                    if sub_index+1 < len(join_split):
                        field_name += '_'
                print('And the field name is ', field_name)
            break
        except BaseException as e:
            print(part, 'not found')
            print('The exception is :')
            print(e)
            pass

    print()
