import pandas as pd
 
test_df = pd.read_csv('./Data/CDHDR_CDPOS_KRED.txt', sep='|', encoding='utf_16_le')

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
                for sub_index, subpart in enumerate(join_split[len(join_split)-len(join_split)+1:len(join_split)]):
                    field_name += subpart                    
                    if sub_index < len(join_split):
                        field_name += '_'
                print('And the field name is ', field_name)
        except:
            print(part, 'not found')
            pass

    print()
    
    

# Possible way of parsing instead of a for loop
print(columns[len(columns)-len(columns)+1])


for something in columns[1:len(columns)]:
    print(something)
