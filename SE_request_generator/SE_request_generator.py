# -*- coding: utf-8 -*-
"""
Created on Sat May  4 17:18:36 2019

@author: ES579DX
"""

import xml.etree.ElementTree as ET

tree = ET.parse('TEST_02.xml')
root = tree.getroot()

print(root.tag)
print(root.attrib)

for child in root:
    print(child.tag, child.attrib)
    
request = root.find('{http://www.audicon.net/DataRequest}Requests')[0]
   
tables = request.findall('{http://www.audicon.net/DataRequest}Table')
for table in tables:
    print(table[0].text, type(table))
    
    

# TO DO:
    # Replace filters