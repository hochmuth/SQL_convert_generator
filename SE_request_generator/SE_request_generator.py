# -*- coding: utf-8 -*-
"""
Created on Sat May  4 17:18:36 2019

@author: ES579DX
"""
import lxml.etree as ET
#import xml.etree.ElementTree as ET
import copy

date_low = '01-01-2018'
date_high = '12-31-2018'
BUKRS = ['B001', 'B002', 'B003']
KKBER = ['KK01', 'KK02', 'KK03']
VKORG = ['V001', 'V002', 'V003']
GJAHR = ['2017', '2018']
FILTER_LIST = [BUKRS, KKBER, VKORG, GJAHR]
FILTER_NAMES = ['BUKRS', 'KKBER', 'VKORG', 'GJAHR']

namespaces = {'ns0' : '{http://www.audicon.net/DataRequest}'}
ns = '{http://www.audicon.net/DataRequest}'

tree = ET.parse('TEST_02.xml')
root = tree.getroot()

def fill_out_filter(root_tree, filter_list, filter_names):
    for i, filter_field in enumerate(filter_list):
        if len(filter_field) > 0:
            for element in root_tree.iter(ns+'Filter'):
                if element.find(ns+'Name').text == FILTER_NAMES[i]:
                    for item in filter_field:
                        copied = copy.deepcopy(element)
                        copied.find(ns+'Low').text = item
                        element.addnext(copied)
                    parent = element.getparent()
                    parent.remove(element)
    return root_tree

def fill_out_dates(root_tree, date_low, date_high):
    for tag in root_tree.iter():
        if (tag.text is not None) and (tag.text.upper() == 'XXXXXXXX'):
            tag.text = date_low    
        if  (tag.text is not None) and (tag.text.upper() == 'YYYYYYYY'):
            tag.text = date_high
    return root_tree



tree = ET.parse('TEST_03.xml')
root = tree.getroot()
                    
output_tree = ET.ElementTree(fill_out_filter(fill_out_dates(root, date_low, date_high), FILTER_LIST, FILTER_NAMES))
output_tree.write('output.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")
   
# TO DO:
    # add VKORG, KKBER, GJAHR