# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 10:19:01 2020

@author: ASUS
"""
import math
import shapefile
import numpy as np
import pandas as pd
import math
from shapely.geometry import LineString,Point    
import pandas as pd
import numpy as np
import datetime
import glob
from datetime import date


# Distance function
def distance_m(location1, location2): # location1 is a list of lat and lon
    lat1, lon1 = location1
    lat2, lon2 = location2
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = radius * c * 1000
    return dist

def within_2(point,line,dist_set): # input point,linestring and set distance in meters
    pt = Point(point)
    p1, p2 = nearest_points(line, pt)
    dist = distance_m([p1.x,p1.y],point)
    if dist <= dist_set:
        return True
    else:
        return False

######################## polyline ###############################################
path = r"G:/.shortcut-targets-by-id/196UCcDxqaoKI3-8-fO-eobfUJakBhSqM/RoadData/"
doh_sf = shapefile.Reader(path + "DOH/DOHRoad")

list_line = [] # save linestring of polyline
polyline = [] # save the polyline
for shape in doh_sf.shapes(): #shape -> one long road
    points = shape.points
    Polyline_doh = [list(ele) for ele in points]  # Polyline : [[lon,lat],[lon,lat],.....] 
    for ele in Polyline_doh:
        ele[0],ele[1] = ele[1],ele[0]  #swap lat,lon
    polyline.append(Polyline_doh)
    line = LineString(Polyline_doh)
    list_line.append(line)
    
################### 1 day log of all vehicles ######################################################
import time
start = time.time()
path =r'G:\.shortcut-targets-by-id\1BMwGDvpAqVWZD7P9pYvgrhsUE0PSUQlV\TC_Research\gps_log\2018-01\2018-01-01_*.zip' 
allFiles = glob.glob(path)
list_ = []
for file_ in allFiles:
    df_file = pd.read_csv(file_, compression='zip')
    list_.append(df_file)
df = pd.concat(list_).reset_index(drop=True)
stop = time.time()
stop-start
df
# df['point'] = df.apply(lambda x: list([x['lat'],x['lon']]),axis=1)    
start = time.time()
df["point"] = df[["lat", "lon"]].values.tolist()
df= df.sort_values(by=['time_stamp'])
df['time_stamp'] = pd.to_datetime(df['time_stamp'])
df = df[(df['time_stamp'] > '2018-01-01 10:00:00') & (df['time_stamp'] < '2018-01-01 13:00:00')]
df
stop = time.time()
stop-start
df = df.reset_index(drop=True)
df
####################### Filter vehicles on road number 2 #################################
from shapely.geometry import LineString,Point,Polygon
from shapely.ops import nearest_points
path = r"G:/.shortcut-targets-by-id/196UCcDxqaoKI3-8-fO-eobfUJakBhSqM/RoadData/"
import pandas as pd
kmdb = pd.read_csv(path+"KM_Data/latlon_km.csv")
kmdb.head(100)
len(kmdb[kmdb['rd']==2])

kmdb_1 = kmdb[kmdb['rd']==2].copy()
kmdb_1
kmdb_1['loc'] = kmdb_1[['lat', 'lon']].apply(list, axis=1)
kmdb_1 = kmdb_1.sort_values(by=['km'])
kmdb_1
list_km = kmdb_1['loc'].values.tolist()
list_km  # a list of kmstone in road number 2
line = LineString(list_km) # make a linestring of road number 2
###########################  50m   ###################################
df
within = []
for i in df.iterrows():
    within.append(within_2(i[1][-1],line,50))
    print( within_2(i[1][-1],line,50))
df_bool = pd.DataFrame(within,columns=['bool']).reset_index(drop=True)
df_bool
len(df)
len(df_bool)
df1 = df.join(df_bool)
df1
df2 = df1[df1['bool'] == True]  # dataframe for the point within 50 meters
df2
df2_out = df1[df1['bool'] == False] # dataframe for the point outside 50 meters
df2_out
df3 = df2[df2['speed'] != 0] # points where speed is not 0
df3
df3_out = df2_out[df2_out['speed'] != 0]
df3_out

df3.columns

len(df3['unit_id'].unique())
df3['unit_id'].value_counts().idxmax()

#####################################  50m from linestring #########################################################
# take one linestring from polyline
line = list_line[0]
line
df   # dataframe containing the gos log for a day
within = []
for i in df.iterrows():
    within.append(within_2(i[1][-1],line,50))
    print( within_2(i[1][-1],line,50)) # print whether true or false (within 50 m or outside)
df_bool = pd.DataFrame(within,columns=['bool']).reset_index(drop=True) # add column of true or false
df_bool
df1 = df.join(df_bool)
df1
df2 = df1[df1['bool'] == True]  # dataframe for the point within 50 meters
df2
df2_out = df1[df1['bool'] == False] # dataframe for the point outside 50 meters
df2_out
df3 = df2[df2['speed'] != 0] # points where speed is not 0
df3
df3_out = df2_out[df2_out['speed'] != 0]
df3_out

df3.columns

len(df3['unit_id'].unique())
df3['unit_id'].value_counts().idxmax()

df2
df2_out
df3
df3
#################### Find the closest km marks ##################################
df3

dist_closest = []  # store the closest distance between the vehicles and the kmstone
for i in df3.iterrows():
    print(i[0])
    print(i[-1][-2])
    for j in kmdb_1
        dist = distance_m(i[-1][-2],j)
        if dist < dist_clostest:
            dist_clostest.pop().append(dist)
        else:
            pass
    break

############################### 30m  ######################################
within_1 = []
for i in df.iterrows():
    within_1.append(within_2(i[1][-1],line,30))
    print( within_2(i[1][-1],line,30))
df_bool_1 = pd.DataFrame(within_1,columns=['bool']).reset_index(drop=True)
df_bool_1
len(df)
len(df_bool_1)
df1_1 = df.join(df_bool_1)
df1_1
df2_1 = df1_1[df1_1['bool'] == True]
df2_1
df3_1 = df2_1[df2_1['speed'] != 0]
df3_1    
    
len(df)

############# visualize ###############

import folium
m = folium.Map(
        location=[13.727876, 100.540474],
        zoom_start=10
    )

# for i in ind:
#     for j in polyline_index:
#         folium.PolyLine(polyline[j[0]], color="blue", weight=2.5, opacity=1).add_to(m)
#         folium.PolyLine(polyline[j[1]], color="blue", weight=2.5, opacity=1).add_to(m) 

# for i in list_km:
#     folium.Circle(
#     radius = 0,
#     location=i,
#     popup=[i],
#     color='crimson'
# ).add_to(m) 
    
# for i in [list_km]:
#     folium.PolyLine(i, color="green", weight=2.5, opacity=1).add_to(m)

for i in [list_line[]]:
    folium.PolyLine(i, color="green", weight=2.5, opacity=1).add_to(m)
    
for i in polyline[0]:
    folium.Circle(
    radius = 0,
    location=i,
    popup=[i],
    color='yellow'
).add_to(m) 
    
# for i in list_km:
#     folium.Circle(
#         radius = 0,
#         location=i,
#         popup=[i],
#         color='black'
#     ).add_to(m) 
    
# for i in df3[df3['unit_id']=='0790006WET05863835029936270' ].iterrows():
#     folium.Circle(
#         radius = 0,
#         location=i[1][-2],
#         popup=[i],
#         color='crimson'
#     ).add_to(m) 

# for i in df3_out[df3_out['unit_id']=='0790006WET05863835029936270' ].iterrows():
#     folium.Circle(
#         radius = 0,
#         location=i[1][-2],
#         popup=[i],
#         color='yellow'
#    ).add_to(m) 
# for i in df2_1[df2_1['unit_id']=='0790006WET05863835029936270' ].iterrows():
#     folium.Circle(
#         radius = 0,
#         location=i[1][-2],
#         popup=[i],
#         color='yellow'
#     ).add_to(m) 
    
# for i in df2_1[df2_1['unit_id']=='0790006WET05863835029936270' ].iterrows():
#     folium.Circle(
#         radius = 0,
#         location=i[1][-2],
#         popup=[i],
#         color='crimson'
#     ).add_to(m) 
    # folium.Marker(
    #     location=i[1][-2],
    #     popup='vehicles',
    #     icon=folium.Icon(icon='cloud')
    # ).add_to(m) 
m
m.save('E:\Transcode'+ "/map-matching.html")   


len(df2_1[df2_1['unit_id']=='0790006WET05863835029936270' ])
len(df2[df2['unit_id']=='0790006WET05863835029936270' ])








