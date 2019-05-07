# -*- coding: utf-8 -*-
"""
Created on Tue May  7 10:55:49 2019

@author: ES579DX
"""
import copy
import lxml.etree as ET

tables_dict = {
        'BKPF' : ['COL1', 'COL2', 'COL3'],
        'BSEG' : ['COL1', 'COL2', 'COL3', 'COL4']
        }

namespaces = {'ns0' : '{http://www.audicon.net/DataRequest}'}
ns = '{http://www.audicon.net/DataRequest}'

root = ET.parse('SAMPLE.xml').getroot()

sample_table = root.find(ns+'Requests').find(ns+'Request').find(ns+'Table')
sample_column = root.find(ns+'Requests').find(ns+'Request').find(ns+'Table').find(ns+'Column')
sample_filter = root.find(ns+'Requests').find(ns+'Request').find(ns+'Table').find(ns+'Filter')


ET.dump(sample_table)
ET.dump(sample_column)
ET.dump(sample_filter)

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
    ET.dump(copied_table)



'''
    TO DO:
        Generate two more tables with some sample columns, plus delete the first one.
'''