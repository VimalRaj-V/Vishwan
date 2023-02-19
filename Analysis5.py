# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 20:09:56 2023

@author: Vimal Raj
"""

import pandas as pd
import numpy as np
import csv

cities = ['Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai']
for city in cities:
    filename = city +".csv"
    data = pd.read_csv(filename)
    data_csv = data.copy()
    
    data_csv.replace(9, "nan", inplace = True)
    Locations = list(np.unique(data_csv["Location"]))
    parameters = list(data_csv.columns)
    
    Avg_price = 0
    cost = {}
    details = {}
    features = {}
    i = 0
    
    for Location in data_csv['Location']:
        if Location not in cost:
            cost[Location] = [[], [], [], [0, 0, 0, 0], 0]
            details[Location] = {}
            features[Location] = {}
            for parameter in parameters[4:]:
                features[Location][parameter] = 0
        cost[Location][0].append(round((data_csv['Price'][i]/data_csv['Area'][i]), 2))
        cost[Location][1].append(data_csv['Area'][i])
        cost[Location][2].append(data_csv['Price'][i])
        n = data_csv['No. of Bedrooms'][i]
        if n == 1:
            cost[Location][3][0] += 1
        elif n == 2:
            cost[Location][3][1] += 1
        elif n == 3:
            cost[Location][3][2] += 1
        else:
            cost[Location][3][3] += 1
        cost[Location][4] += 1
        
        for parameter in parameters[4:]:
            if data_csv[parameter][i] == 1:
                features[Location][parameter] += 1
        i += 1
        
        
    for loc_name in cost.keys():
        selling_cost = cost.get(loc_name)[0]
        
        selling_cost.sort()
        details[loc_name]['max_selling_cost'] = max(selling_cost)         # maximum selling cost
        details[loc_name]['avg_selling_cost'] = np.mean(selling_cost)     # mean selling cost
        details[loc_name]['min_selling_cost'] = min(selling_cost)         # minimum selling cost
        
        y = np.array(cost.get(loc_name)[2])
        selling_area = cost.get(loc_name)[1]
        x = np.array(selling_area.copy())
        selling_area.sort()
        
        details[loc_name]['max_selling_area'] = max(selling_area)        # maximum selling area
        details[loc_name]['avg_selling_area'] = np.mean(selling_area)    # mean selling area
        details[loc_name]['min_selling_area'] = min(selling_area)        # minimum selling area
    
    
    # writing to csv file 
    filename2 = "processed_data_" + city + ".csv"
    fields = ['sl_no', 'location', 'no_of_houses_surveyed', 'max_selling_cost', 'avg_selling_cost', 'min_selling_cost', 'max_selling_area', 'avg_selling_area', 'min_selling_area', '1bhk', '2bhk', '3bhk', '3+bhk']
    for parameter in parameters[4:]:
        fields.append(parameter)
    with open(filename2, 'w',newline = '') as csvfile:
        
        csvwriter = csv.writer(csvfile)  
        csvwriter.writerow(fields)
        # writing the data rows 
        i = 0
        for loc_name in Locations:
            detail = [i,loc_name, cost[loc_name][4], details[loc_name]['max_selling_cost'], details[loc_name]['avg_selling_cost'], details[loc_name]['min_selling_cost'],
                      details[loc_name]['max_selling_cost'], details[loc_name]['avg_selling_area'], details[loc_name]['min_selling_area'], cost[loc_name][3][0], cost[loc_name][3][1], cost[loc_name][3][2], cost[loc_name][3][3]]
            for parameter in parameters[4:]:
                detail.append(features[loc_name][parameter])
            csvwriter.writerow(detail)
            i += 1
        