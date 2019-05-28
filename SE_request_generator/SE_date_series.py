# -*- coding: utf-8 -*-
"""
Created on Mon May 27 16:22:58 2019

"""
import os
import lxml.etree as ET

from datetime import datetime, timedelta
from SE_replace_filters import fill_out_dates

first_date = '20180201'
last_date = '20180331'
increment_by = 2

input_file = 'TEST_03.xml'

# Needs to be a valid date range
assert datetime.strptime(first_date, '%Y%m%d') < datetime.strptime(last_date, '%Y%m%d')

# Get the file name without extension
tmp_name = os.path.splitext(input_file)[0]
fname = os.path.basename(tmp_name)

# Main loop
orig_date = first_date
while datetime.strptime(orig_date, '%Y%m%d') <= datetime.strptime(last_date, '%Y%m%d'):    
    added_low = orig_date
    added_high = (datetime.strptime(orig_date, '%Y%m%d') + timedelta(days=increment_by)).strftime('%Y%m%d')
    print('Low', added_low)
    print('High', added_high)    
    orig_date = (datetime.strptime(added_high, '%Y%m%d') + timedelta(days=1)).strftime('%Y%m%d')
    
    tree = ET.parse(input_file)    
    root = tree.getroot()
    
    output_tree = ET.ElementTree(fill_out_dates(root, added_low, added_high))
    output_tree.write('./date_range_test/' + fname + '_' + added_low + '.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")