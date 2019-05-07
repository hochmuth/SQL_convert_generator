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
ns = '{http://www.audicon.net/DataRequest}'

tree = ET.parse('TEST_02.xml')
root = tree.getroot()

# Look at what we've got
ET.dump(root)
print()
    
#request = root.find(ns+'Requests').find(ns+'Request')   
#tables = request.findall(ns+'Table')


for item in root.iter(ns+'Filter'):
#    print(item.find('..'))
        
    if item.find(ns+'Name').text == 'BUKRS':
        for element in BUKRS:
            copied = copy.deepcopy(item)
            copied.find(ns+'Low').text = element
            item.addnext(copied)
        parent = item.getparent()
        parent.remove(item)
        

ET.dump(root)

output_tree = ET.ElementTree(root)
output_tree.write('output.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")
   
#for copied in copies:
#    ET.dump(copied)


# TO DO:
    # Delete the first filter element