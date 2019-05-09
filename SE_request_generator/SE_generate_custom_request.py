# -*- coding: utf-8 -*-
"""
Created on Tue May  7 10:55:49 2019

@author: ES579DX
"""
import copy
import lxml.etree as ET
import pandas as pd

out_file_name = 'SE_custom_request'

namespaces = {'ns0' : '{http://www.audicon.net/DataRequest}'}
ns = '{http://www.audicon.net/DataRequest}'


def populate_xml(root_tree, tables_dict, filters=False):
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
        if not filters:
            copied_filter = copied_table.find(ns+'Filter')
            copied_table.remove(copied_filter)
        sample_table.addprevious(copied_table)    
        
    sample_parent = sample_table.getparent()
    sample_parent.remove(sample_table)
    
    return root_tree

if __name__ == '__main__':

    tables_dict = {}    
    excel = pd.read_excel('Tables_and_fields.xlsx', sheet_name='Final_List', header=0, names=['Table', 'Field'])
    
    # Get all relevant table names and populate the dictionary
    table_list = excel.Table.unique()
    for table in table_list:        
        relevant_fields = excel.loc[excel['Table'] == table]
        field_list = []
        for relevant_field in relevant_fields.Field.unique():
            field_list.append(str(relevant_field).strip())
        tables_dict[str(table)] = field_list
        
    
    # Generate the new xml file and save into a file
    root = ET.parse('SAMPLE.xml').getroot()    
    output_tree = ET.ElementTree(populate_xml(root, tables_dict))
    output_tree.write(out_file_name+'.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")

'''
    TO DO:
        Test it.   
'''