# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 11:50:06 2020

@author: ASUS
"""
############# find road number 9 from kmstone file    ################

from shapely.geometry import LineString,Point,Polygon
from shapely.ops import nearest_points
path = r"G:/.shortcut-targets-by-id/196UCcDxqaoKI3-8-fO-eobfUJakBhSqM/RoadData/"
import pandas as pd
kmdb = pd.read_csv(path+"KM_Data/latlon_km.csv")
kmdb.head(100)
kmdb1 = kmdb[kmdb['rd']==9].copy()
kmdb1

kmdb1['loc'] = kmdb1[['lat', 'lon']].apply(list, axis=1)
kmdb1['loc'] = kmdb1['loc'].apply(lambda x:[round(i,3) for i in x] )
kmdb_g = kmdb1.groupby('rd').agg(lambda x: x.tolist())
kmdb_g
kmdb_g.columns
kmdb_g = kmdb_g.drop(['lat','lon'],axis=1)
kmdb_g
kmdb_g['loc']
list_km = kmdb_g['loc'].values[0]
list_km
#########################3
def find_max(list):
    num =[]
    count = 0
    for i in list:
        if list.count(i) > count and i not in num:
            num =[i]
            count = list.count(i)
        elif list.count(i) == count and i not in num:
            num.append(i)
            count = list.count(i)
        else:
            pass

    return num,count

########### shapefile #############
import shapefile    
path = r"G:/.shortcut-targets-by-id/196UCcDxqaoKI3-8-fO-eobfUJakBhSqM/RoadData/"
doh_sf = shapefile.Reader(path + "DOH/DOHRoad")
polyline_9 = []
index =[]
count = 0
for shape in doh_sf.shapes(): #shape -> one long road
    points = shape.points
    Polyline_doh = [list(ele) for ele in points]  # Polyline : [[lon,lat],[lon,lat],.....] 
    Polyline_round = [list(ele) for ele in points]
    for ele in Polyline_doh:
        ele[0],ele[1] = ele[1],ele[0] #swap lat,lon
    for ele in Polyline_round:
        ele[0],ele[1] = round(ele[1],3),round(ele[0],3) #swap lat,lon    
    list_rd = [] # storing a list of matched road number for each polyline
    for i in Polyline_round:
        if i in list_km:
            list_rd.append(9)
        else:
            pass
    if find_max(list_rd)[1]>5:
        polyline_9.append(Polyline_doh)
        index.append(count)
        print("this is road no.9")
    else:
        pass
    count+=1
index
################# visually verify road number 9 ##############
import folium
m = folium.Map(
        location=[13.727876, 100.540474],
        zoom_start=10
    )


folium.PolyLine(polyline_9[0], color="green", weight=2.5, opacity=1).add_to(m)

m
m.save('E:\Transcode'+ "/roadnumber9.html")   

#################
import glob
path =r'G:\.shortcut-targets-by-id\1BMwGDvpAqVWZD7P9pYvgrhsUE0PSUQlV\TC_Research\gps_log\2018-01\2018-01-01_*.zip' 
allFiles = glob.glob(path)
list_ = []
for file_ in allFiles:
    df_file = pd.read_csv(file_, compression='zip')
    list_.append(df_file)
df = pd.concat(list_).reset_index(drop=True)
df
# df['point'] = df.apply(lambda x: list([x['lat'],x['lon']]),axis=1)    
df["point"] = df[["lat", "lon"]].values.tolist()
df= df.sort_values(by=['time_stamp'])
df['time_stamp'] = pd.to_datetime(df['time_stamp'])
df = df[(df['time_stamp'] > '2018-01-01 10:00:00') & (df['time_stamp'] < '2018-01-01 13:00:00')]
df
df = df.reset_index(drop=True)
df

############## find linestring of no.9 ###############
line = LineString(polyline_9[0]) 
line

#######################
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

within = []
for i in df.iterrows():
    within.append(within_2(i[1][-1],line,30))
    print( within_2(i[1][-1],line,30))
df_bool = pd.DataFrame(within,columns=['bool']).reset_index(drop=True)
df_bool
df1 = df.join(df_bool)
df1
df2 = df1[(df1['bool'] == True) & (df1['speed'] != 0)].reset_index().drop(['index'],axis=1)  # dataframe for the point within 50 meters
df2
df2_out = df1[(df1['bool'] == False) & (df1['speed'] != 0)] # dataframe for the point outside 50 meters
df2_out
df2['unit_id'].value_counts().idxmax()
df2.columns

nearest_point = []
for i in df2['point'].tolist():
    pt = Point(i)
    p1, p2 = nearest_points(line, pt)
    nearest_point.append([[p1.x,p1.y]])
    
np = pd.DataFrame(nearest_point,columns=['nearest_point'])
np
df3 = pd.concat([df2,np],axis=1)

###### visualize #########3
import folium
m = folium.Map(
        location=[13.727876, 100.540474],
        zoom_start=10
    )

folium.PolyLine(polyline_9[0], color="green", weight=2.5, opacity=1).add_to(m)

# for i in df2[df2['unit_id']=='0790001000004210178584'].iterrows():
#     folium.Circle(
#         radius = 0,
#         location=i[1][-2],
#         popup=[i],
#         color='crimson'
#     ).add_to(m) 
  
for i in df3.iterrows(): 
    folium.Circle(
        radius = 0,
        location=i[1][-3], # raw
        popup=[i],
        color='blue'
        ).add_to(m) 
    folium.Circle(
        radius = 0,
        location=i[1][-1],
        popup=[i],
        color='green'     #closest
    ).add_to(m) 
    link = [i[1][-3],i[1][-1]]
    folium.PolyLine([link], color="red", weight=2.5, opacity=1).add_to(m)
    
m
m.save('E:\Transcode'+ "/roadnumber9.html") 







