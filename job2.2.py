# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:10:06 2020

@author: ASUS
"""

####################### DISTANCE FUNCTION #####################################
def distance_km(location1, location2): # location1 is a list of lat and lon
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

import shapefile
import numpy as np
import pandas as pd
import math


path = r"G:/.shortcut-targets-by-id/196UCcDxqaoKI3-8-fO-eobfUJakBhSqM/RoadData/"
doh_sf = shapefile.Reader(path + "DOH/DOHRoad")

list_marks = []
POLYLINE = []

for shape in doh_sf.shapes(): #shape -> one long road
    points = shape.points
    Polyline_doh = [list(ele) for ele in points]  # Polyline : [[lon,lat],[lon,lat],.....] 
    for ele in Polyline_doh:
        ele[0],ele[1] = ele[1],ele[0]  #swap lat,lon
    p1 =  Polyline_doh[0] 
    p2 =  Polyline_doh[1]
    km_st = [Polyline_doh[0]]
    count = 0  # keep track of poles
    trav = 0
    pin  = [Polyline_doh[0]]
    while p1 != Polyline_doh[-1]:
        if distance_km(pin[-1],p2) > 100:
            lat_k = (100/distance_km(p2,p1))*(p2[0]-p1[0])+km_st[-1][0] 
            lon_k = (100/distance_km(p2,p1))*(p2[1]-p1[1])+km_st[-1][1] 
            pin.append([lat_k,lon_k])
            km_st.append([lat_k,lon_k])
            print(km_st[-1],'A',distance_km(km_st[-1],km_st[-2]))

        elif distance_km(pin[-1],p2) == 100:
            pin.append(p2)
            km_st.append(p2)
            print(km_st[-1],'B',distance_km(km_st[-1],km_st[-2]))
            count+=1
            try:
                p1 = Polyline_doh[count]
                p2 = Polyline_doh[count+1]
            except IndexError:
                break   
        else: # distance_km(pin[-1],p2) < 100
            while True:
                if trav+distance_km(pin[-1],p2) < 100:
                   trav += distance_km(pin[-1],p2) 
                   pin.append(p2)
                   count+=1
                   try:
                       p1 =  Polyline_doh[count] 
                       p2 =  Polyline_doh[count+1]
                   except IndexError:
                       break
                elif trav+distance_km(pin[-1],p2) == 100:
                    km_st.append(p2)
                    pin.append(p2)
                    print(km_st[-1],'C',distance_km(km_st[-1],km_st[-2]))
                    break
    
                else : # trav+distance_km(pin[-1],p2) > 100:
                    dist_left = 100 - trav
                    lat_k = (dist_left/distance_km(p1,p2))*(p2[0]-p1[0])+p1[0] 
                    lon_k = (dist_left/distance_km(p1,p2))*(p2[1]-p1[1])+p1[1] 
                    km_st.append([lat_k,lon_k])
                    pin.append([lat_k,lon_k])
                    trav = 0
                    print(km_st[-1],'D',distance_km(km_st[-1],km_st[-2]))
                    break

    
    list_marks.append(km_st)                
    POLYLINE.append(Polyline_doh)
list_marks[0]         
list_marks[1]  
len(POLYLINE[0])
#################### test the distance between each 100m marks #########################
for i in range(len(list_marks[1])-1):
    print(distance_km(list_marks[0][i],list_marks[0][i+1]))    
                
import folium
m = folium.Map(
        location=[13.727876, 100.540474],
        zoom_start=10
    )

for i in list_marks[1]:
    folium.Circle(
    location=i,
    radius=1,
     ).add_to(m)
    
Polyline_doh

for i in [Polyline_doh]:
    folium.PolyLine(i, color="green", weight=2.5, opacity=1).add_to(m)
    
m
m.save('E:\Transcode'+ "/try3.html")                    

################################################################################3                
# map the 100 marks with road number

###############################################
############################# DICTIONARY ################################################


import pandas as pd
kmdb = pd.read_csv(path+"KM_Data/latlon_km.csv")
kmdb.head()
kmdb.shape
kmdb.head()
kmdb['loc'] = kmdb[['lat', 'lon']].apply(list, axis=1)
kmdb['loc'] = kmdb['loc'].apply(lambda x:[round(i,3) for i in x] ) # round dictionary to 4 decimal places
try:
    kmdb = kmdb.drop(['lat','lon'],axis=1)
except KeyError:
    print("already dropped")
kmdb_1 = kmdb.groupby('rd').agg(lambda x: x.tolist())
dict = {k: v["loc"].tolist() for k,v in kmdb.groupby("rd")}
print(kmdb.head())
dict
###################################### FIND MAX ####################################################

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

###################################  CREATE A DATAFRAME ###################################################
list_of_tuples = list(zip(list_marks, POLYLINE))  
len(POLYLINE)    
df_DOH = pd.DataFrame(list_of_tuples,columns=['list_marks','polyline'])   
df_DOH.head()

#################################### round #######################
def round_(x):
    for i in x:
        i[0],i[1] = round(i[0],3),round(i[1],3)
    return x
    
df_DOH['marks_round'] = df_DOH['list_marks'].apply(round_)
df_DOH['marks_round']

df_DOH


################################ MAPPING TO GET ROAD NUMBER ######################################
rd = []
index = []
count = 0
for mark in df_DOH['marks_round']:
   road = []
   for key in dict: # key is the road number
       for p in mark: 
           if p in dict[key]:
               road.append(key) #if the cross in that dict[road number]->append the road number
           else:
               pass
   if find_max(road)[1] >5: # if the road umber appears more than five times in polyline,its likely to be that road
       rd.append(find_max(road)[0])
       index.append(count)
       #polyline.append(mark) #only append the polyline where we know the road number
       print(find_max(road)[0])
   else:
       pass 
   count+=1
   print('number of time: ',count)
   
 
############################## CREATE A FINAL DATAFRAME #################################

rd
index

df3 =  pd.DataFrame(list(zip(rd,index)),columns=['road number','index'])
df3

df4 =  pd.DataFrame(list(zip(np.array([i for i in range(len(POLYLINE))]),POLYLINE)),columns=['index','polyline'])
df4
len(df4['polyline'][0])
df5 = pd.merge(df3,df4,on='index',how='left')
df5
df6 = df5.drop(columns=['index'])
df6


df6['polyline'][1]
len(df6['polyline'][0])

df6.to_csv(r'E:\Transcode\job2.2.csv')
len(df6['polyline'][0])

df6

############################## FIND THE INTERSECTION #############################

df6   

import shapely
from shapely.geometry import LineString
road = []
POLY =[]
for i in range(len(df6['polyline'])):
    line_a = LineString(df6['polyline'][i])
    store = [df6['road number'][i]]
    poly = [df6['polyline'][i]]
    for j in range(len(df6['polyline'])):
        line_b = LineString(df6['polyline'][j])
        if line_a != line_b and (line_a.intersects(line_b) == True)\
           and (df6['road number'][j] not in store):
            store.append(df6['road number'][j])   #storing road number
            poly.append(df6['polyline'][j])     # store polyline
            print(store,i,j)      
        else: pass
    if len(store) > 1:
        road.append(store)
        POLY.append(poly)
    else:pass
    break
road
POLY[0]
df6['road number'][j]

#### 3309 347 and 9

########################### Visualize intersection #################################
df6[:20]
df6['road number'][0]
df6['polyline'][0]
df6['road number'][10]
df6['polyline'][10]
a = LineString(df6['polyline'][0])
b = LineString(df6['polyline'][98])
a.intersects(b)

int_pt = a.intersection(b)
point_of_intersection =int_pt.x, int_pt.y
intersect = list(point_of_intersection)
intersect



import folium
m = folium.Map(
        location=[13.727876, 100.540474],
        zoom_start=10
    )

for i in [df6['polyline'][0]]:
    folium.PolyLine(i, color="green", weight=2.5, opacity=1).add_to(m)
for i in [df6['polyline'][98]]:
    folium.PolyLine(i, color="red", weight=2.5, opacity=1).add_to(m)
folium.Marker(
    location=intersect,
    popup=intersect,
    icon=folium.Icon(icon='cloud')
).add_to(m)    

a = LineString(df6['polyline'][1])
b = LineString(df6['polyline'][79])
a.intersects(b)

int_pt2 = a.intersection(b)
point_of_intersection2 =int_pt2.x, int_pt2.y
intersect2 = list(point_of_intersection2)
intersect2


for i in [df6['polyline'][1]]:
    folium.PolyLine(i, color="green", weight=2.5, opacity=1).add_to(m)
for i in [df6['polyline'][79]]:
    folium.PolyLine(i, color="red", weight=2.5, opacity=1).add_to(m)
folium.Marker(
    location=intersect2,
    popup=intersect2,
    icon=folium.Icon(icon='cloud')
).add_to(m)    
m
m.save('E:\Transcode'+ "/cross.html")       
################################################################

import folium
m = folium.Map(
        location=[13.727876, 100.540474],
        zoom_start=10
    )

for i in [df6['polyline'][1]]:
    folium.PolyLine(i, color="green", weight=2.5, opacity=1).add_to(m)
    
m
m.save('E:\Transcode'+ "/polyline[0].html")      
########################################
rd = []
index = []
count = 0
for mark in df_DOH['marks_round']:
   road = []
   for key in dict: # key is the road number
       for p in mark: 
           if p in dict[key]:
               road.append(key) #if the cross in that dict[road number]->append the road number
           else:
               pass
   if find_max(road)[1] >5: # if the road umber appears more than five times in polyline,its likely to be that road
       rd.append(find_max(road)[0])
       index.append(count)
       #polyline.append(mark) #only append the polyline where we know the road number
       print(find_max(road)[0])
   else:
       pass 
   count+=1
   print('number of time: ',count)
   
index
#################################




