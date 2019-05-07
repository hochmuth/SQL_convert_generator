# -*- coding: utf-8 -*-
"""
Created on Tue May  7 10:55:49 2019

@author: ES579DX
"""
import copy
import lxml.etree as ET

namespaces = {'ns0' : '{http://www.audicon.net/DataRequest}'}
ns = '{http://www.audicon.net/DataRequest}'

root = ET.parse('SAMPLE.xml').getroot()

sample_table = root.find(ns+'Requests').find(ns+'Request').find(ns+'Table')
sample_column = root.find(ns+'Requests').find(ns+'Request').find(ns+'Table').find(ns+'Column')
sample_filter = root.find(ns+'Requests').find(ns+'Request').find(ns+'Table').find(ns+'Filter')


ET.dump(sample_table)
ET.dump(sample_column)
ET.dump(sample_filter)



'''
    TO DO:
        From an example SE request:
            get sample table (empty)
            get sample column
            get sample filter
'''