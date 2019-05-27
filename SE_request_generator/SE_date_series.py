# -*- coding: utf-8 -*-
"""
Created on Mon May 27 16:22:58 2019

@author: ES579DX
"""

from datetime import datetime, timedelta

first_date = '20180101'
last_date = '20180131'
increment_by = 10

orig_date = first_date
while datetime.strptime(orig_date, '%Y%m%d') <= datetime.strptime(last_date, '%Y%m%d'):    
    added_low = orig_date
    added_high = (datetime.strptime(orig_date, '%Y%m%d') + timedelta(days=increment_by)).strftime('%Y%m%d')
    print('Low', added_low)
    print('High', added_high)    
    orig_date = (datetime.strptime(added_high, '%Y%m%d') + timedelta(days=1)).strftime('%Y%m%d')