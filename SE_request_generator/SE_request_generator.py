# -*- coding: utf-8 -*-
"""
Created on Sat May  4 17:18:36 2019

@author: ES579DX
"""
import lxml.etree as ET
#import xml.etree.ElementTree as ET
import copy

BUKRS = ['B001', 'B002', 'B003']

namespaces = {'ns0' : '{http://www.audicon.net/DataRequest}'}

tree = ET.parse('TEST_02.xml')
root = tree.getroot()

# Look at what we've got
ET.dump(root)
    
request = root.find('{http://www.audicon.net/DataRequest}Requests').find('{http://www.audicon.net/DataRequest}Request')
   
tables = request.findall('{http://www.audicon.net/DataRequest}Table')

copies = []
for item in root.iter('{http://www.audicon.net/DataRequest}Filter'):
    print(item.find('..'))
        
    if item.find('{http://www.audicon.net/DataRequest}Name').text == 'BUKRS':
        for element in BUKRS:
            copied = copy.deepcopy(item)
            copied.find('{http://www.audicon.net/DataRequest}Low').text = element
#           copies.append(copied)
            item.addnext(copied)
        

ET.dump(root)
   
#for copied in copies:
#    ET.dump(copied)


# TO DO:
    # Delete the first filter element