# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 12:12:35 2020

@author: ASUS
"""


############ GRID VISUALIZATIOn ################


import pandas as pd 
gps = pd.read_csv("G:\My Drive\km_n_newlag.csv", encoding='iso8859_11',delimiter=';')
gps.head()
gps_sam = gps.head(100).copy()

print("length of data: ",len(gps))
gps['km_label,'].head(5)
gps['km_label,'].replace(',',' ')
gps.head()
gps['km_label,'] = gps['km_label,'].str[:3]
import re
def find_num(string):
    temp = re.findall(r'\d+', string) 
    res = list(map(int, temp)) 
    return int(res[0])
gps['km_label,'] = gps['km_label,'].apply(find_num)
gps.dtypes
gps

kmst = [[2,143,151],[1,52,56],[304,21,29],[4,18,25],[35,9,21],[340,49,38],[1,62,52],\
        [2,142,150],[9,24,31]]
for i in kmst:
    if i[1]>i[2]:
        i[1],i[2] = i[2],i[1]
    else:
        pass

import folium
m = folium.Map(
        location=[14.9796921903,102.087999633],
        zoom_start=10
    )
for i in kmst:
    for j in range(i[1],i[2]):
        km = gps[(gps['route'] ==i[0]) & (gps['km_label,']==j)]
        point = [km['km_latitude'].values[0],km['km_longitude'].values[0]]
        point_round = [round(point[0],2),round(point[1],2)]
        c1 = [point_round[0]+0.005,point_round[1]+0.005]
        c2 = [point_round[0]-0.005,point_round[1]-0.005]
        c3 = [point_round[0]+0.005,point_round[1]-0.005]
        c4 = [point_round[0]-0.005,point_round[1]+0.005]
        grid = [c4,c1,c3,c2,c4]
    
        folium.Marker(point, popup=(i[0],j)).add_to(m)
    
        # folium.Circle(
        #         radius = 0,
        #         location=point_round,
        #         color='green'     #closest
        #     ).add_to(m) 
        
        # folium.Circle(
        #         radius = 0,
        #         location=grid[0],
        #         color='green'     #closest
        #     ).add_to(m) 
        # folium.Circle(
        #         radius = 0,
        #         location=grid[1],
        #         color='green'     #closest
        #     ).add_to(m) 
         
        folium.PolyLine(grid, color="red", weight=2.5, opacity=1).add_to(m)
        # for i in grid:
        #     folium.PolyLine([i], color="red", weight=2.5, opacity=1).add_to(m)
        m
        m.save('E:\Transcode'+ "/grid.html") 


import math
def distance_m(location1, location2): # location1 is a list of lat and lon
    lat1, lon1 = location1
    lat2, lon2 = location2
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = (radius * c)*1000
    return dist


print(distance_m(c4,c1))
print(distance_m(c1,c3))
print(distance_m(c3,c2))
print(distance_m(c2,c4))


    



