import pandas as pd

dd03l_path = r'c:\temp_DATA\KraftHeinz\CCM_Monthly\Data\Converted\EU\DD03L.csv'
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
                        # Look for it's data type here
                        return table, field_name
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
    
def main():
    # Test table stored in a DataFrame
    test_df = pd.read_csv('./Data/TEST.txt', sep='|', encoding='utf_16_le')
    Searcher = DataTypeSearcher(dd03l_path, dd03l_enc)
    file_name = 'TEST'
    columns = []
    
    for column in test_df:
        dtype = ''    
        columns.append(column.strip())
                
    for column in columns:
        print('Searching in file ', file_name, ', column', column)
        dtype = Searcher.get_field_type(file_name, column)
        print('Method returned the type:', dtype)
        print()
        
if __name__ == "__main__":
    main()
            
        
        
