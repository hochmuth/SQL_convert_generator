# -*- coding: utf-8 -*-
"""
Created on Tue May  7 10:55:49 2019

@author: ES579DX
"""
import copy
import lxml.etree as ET
import pandas as pd

tables = {
        'BKPF' : ['COL1', 'COL2', 'COL3'],
        'BSEG' : ['COL1', 'COL2', 'COL3', 'COL4']
        }

namespaces = {'ns0' : '{http://www.audicon.net/DataRequest}'}
ns = '{http://www.audicon.net/DataRequest}'


def populate_xml(root_tree, tables_dict):
    sample_table = root_tree.find(ns+'Requests').find(ns+'Request').find(ns+'Table')
    sample_column = root_tree.find(ns+'Requests').find(ns+'Request').find(ns+'Table').find(ns+'Column')
    #sample_filter = root_tree.find(ns+'Requests').find(ns+'Request').find(ns+'Table').find(ns+'Filter')
    
    for key in tables_dict:
        copied_table = copy.deepcopy(sample_table)
        copied_table.find(ns+'Name').text = key
        orig_column = copied_table.find(ns+'Column')
        for item in tables_dict[key]:
            # Generate a new column
            copied_column = copy.deepcopy(sample_column)
            copied_column.find(ns+'Name').text = item
            # Append the new column        
            orig_column.addprevious(copied_column)
        copied_table.remove(orig_column)    
        sample_table.addprevious(copied_table)
        
    sample_parent = sample_table.getparent()
    sample_parent.remove(sample_table)
    
    return root_tree

if __name__ == '__main__':
    
    
    excel = pd.read_excel('Tables_and_fields.xlsx', sheet_name='Final_List', header=0, names=['Table', 'Field'])
    print(excel.head())
    # Not the way to go
    pivot = excel.reset_index().to_dict(orient='list')
    
    # Get all relevant table names
    table_list = excel.Table.unique()
    print(table_list)
    
    
    root = ET.parse('SAMPLE.xml').getroot()    
    output_tree = populate_xml(root, tables)
#    ET.dump(output_tree)



'''
    TO DO:
        Figure out how to get the list of field/tables.
        Disregard the filters and joins for now.
'''