# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 19:46:24 2015

@author: Brendan
"""

import os
import csv

# assign variable
precipitation = os.path.abspath("/Users/Brendan/landscape_evolution/Harmon_Brendan_LAKE_Minute_Precip.txt")
    
# open txt file with precipitation data
with open(precipitation) as csvfile:
        # check for header
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)  # rewind
        if has_header:
            next(csvfile)
        # parse time and precipitation
        precip = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
        
        initial=next(precip)
        start=initial[0]
        rain=float(initial[1])
        # run model once to prime it
        
        for row in precip:       
            start=row[0]
            rain=float(row[1])
            
            
            
"""
with open('first.csv', 'rb') as inp, open('first_edit.csv', 'wb') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        if row[2] != "0":
            writer.writerow(row)
"""