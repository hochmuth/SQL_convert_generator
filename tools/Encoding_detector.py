# -*- coding: utf-8 -*-
"""
Parses all relevant text files in a folder and attempts to detect the correct encoding.
"""

import glob
from chardet.universaldetector import UniversalDetector

data_dir = r''
filetype = 'csv'

def get_encoding(file_path):
    detector = UniversalDetector()
    detector.reset()
    for line in open(file_path, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    if detector.result['confidence'] == 1.0:
        return str(detector.result['encoding'])
    else:
        return 'Unknown encoding'
        


if __name__ == '__main__':    
    
    file_list = []
    results = dict()
    
    for filename in glob.glob(data_dir+'\*.'+filetype):    
        file_list.append(filename)
    
    for file in file_list:
        enc = get_encoding(file)
        results.update({str(file) : enc})

    # Print the results    
    for key, item in results.items():
        print('{:60}{}'.format(key, item))