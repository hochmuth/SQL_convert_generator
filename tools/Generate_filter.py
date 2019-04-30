# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 13:03:54 2019

"""

def generate_filter(in_scope_args, out_file, field='BUKRS'):
    for arg in in_scope_args:
        out_file.write('<Filter>\n')
        out_file.write('<Name>'+field+'</Name>\n')
        out_file.write('<Mandatory>false</Mandatory>\n')
        out_file.write('<Sign>I</Sign>\n')
        out_file.write('<Option>EQ</Option>\n')
        out_file.write('<Low>'+arg+'</Low>\n')
        out_file.write('<SmartExporterIgnore>false</SmartExporterIgnore>\n')
        out_file.write('</Filter>\n')
        out_file.write('\n')

if __name__ == '__main__':
    in_scope_arguments = []
    
    out_file = open('filter.txt', 'w', encoding='utf8')
    generate_filter(in_scope_arguments, out_file, field='WERKS')
    out_file.close()      
