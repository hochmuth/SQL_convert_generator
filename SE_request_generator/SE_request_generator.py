# -*- coding: utf-8 -*-
"""
Created on Sat May  4 17:18:36 2019

@author: ES579DX
"""

import xml.etree.ElementTree as ET
import copy

tree = ET.parse('TEST_02.xml')
root = tree.getroot()

ET.dump(root)

#print(root.tag)
#print(root.attrib)
    
request = root.find('{http://www.audicon.net/DataRequest}Requests')[0]
   
tables = request.findall('{http://www.audicon.net/DataRequest}Table')
for table in tables:
    print(table[0].text, table.tag, type(table))
    print(table[1].tag)
    
for table in tables:
    if table[1].text == 'Filter':
        print(table[0].text, table[1].text)

req = root.find('{http://www.audicon.net/DataRequest}Requests')
ET.dump(req)
req_inner = req.find('{http://www.audicon.net/DataRequest}Request')
#print(req_inner)
ET.dump(req_inner)

copies = []
for item in root.iter('{http://www.audicon.net/DataRequest}Filter'):
    ET.dump(item)
    copied = copy.deepcopy(item)
    copies.append(copied)
    if item.find('{http://www.audicon.net/DataRequest}Name').text == 'BUKRS':
        item.find('{http://www.audicon.net/DataRequest}Low').text = 'DDDD'
    
ET.dump(root)


    
    
    

# TO DO:
    # Replace filters