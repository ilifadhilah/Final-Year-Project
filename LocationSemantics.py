
# coding: utf-8

# In[1]:

import pandas as pd
from PIL import Image
import glob
from matplotlib import pyplot as plt
import re
import requests
import json
import cv2
import base64
import os
import numpy as np
from time import sleep
import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn


# ## Open all data, get time, 

# In[2]:

path= "C:/Users/User/Documents/FYP/Extracted Data/"

with open(os.path.join(path, "ExtractedData_Subject1Set1.txt"), 'r') as outfile:
    data_1=json.load(outfile)
    
with open(os.path.join(path, "ExtractedData_Subject1Set2.txt"), 'r') as outfile:
    data_2=json.load(outfile)
    
with open(os.path.join(path, "ExtractedData_Subject1Set3.txt"), 'r') as outfile:
    data_3=json.load(outfile)
    
with open(os.path.join(path, "ExtractedData_Subject1Set4.txt"), 'r') as outfile:
    data_4=json.load(outfile)
    
with open(os.path.join(path, "ExtractedData_Subject1Set5.txt"), 'r') as outfile:
    data_5=json.load(outfile)
    
    
    
time_list_1=[]
time_list_2=[]
time_list_3=[]
time_list_4=[]
time_list_5=[]

for filename in glob.glob('C:\\Users\\User\\Documents\\FYP\\EDUB-Seg\\images\\Subject1_Set1/*.jpg'): 
    time_list_1.append(filename[58:64])

for filename in glob.glob('C:\\Users\\User\\Documents\\FYP\\EDUB-Seg\\images\\Subject1_Set2/*.jpg'): 
    time_list_2.append(filename[58:64])
    
for filename in glob.glob('C:\\Users\\User\\Documents\\FYP\\EDUB-Seg\\images\\Subject1_Set3/*.jpg'): 
    time_list_3.append(filename[58:64])
    
for filename in glob.glob('C:\\Users\\User\\Documents\\FYP\\EDUB-Seg\\images\\Subject1_Set4/*.jpg'): 
    time_list_4.append(filename[58:64])
    
for filename in glob.glob('C:\\Users\\User\\Documents\\FYP\\EDUB-Seg\\images\\Subject1_Set5/*.jpg'): 
    time_list_5.append(filename[67:73])
    


# ## Create dataframes

# In[77]:

nonLocations=['wall', 'light', 'ceiling', 'window', 'plant', 'sign', 'sunglasses', 'brick', 'gauge', 'lamp', 'man', 'water', 'cup', 'dog', 'glasses']

def mainDataframe(df, time_list, data):
    for i in range(len(time_list)):
        try:
            df.loc[i] = [time_list[i], data[i]['tags'] ]
        except:
            df.loc[i]= [time_list[i], 'null']
            
    
    for i in range(len(df)):
        try:
            for j in range(len(df['Tags'][i])):
                if df['Tags'][i][j]['confidence'] <0.75 or df['Tags'][i][j]['name'] in nonLocations:
                    del df['Tags'][i][j]
        except:
            pass
        
        
            
def classifyLocation(tag):
    if tag['name'] == 'indoor' or tag['name'] == 'outdoor':
        df_places[k]['InOut'][i]=tag['name']
    else: 
        for synset in wn.synsets(tag['name']):
            if synset.lexname()=='noun.artifact' or synset.lexname()=='noun.location':
                locations_list.append(tag['name'])
                break
                
                
                


# In[74]:

columns=['Time', 'Tags']

df_1 = pd.DataFrame(columns=columns)
df_2 = pd.DataFrame(columns=columns)
df_3 = pd.DataFrame(columns=columns)
df_4 = pd.DataFrame(columns=columns)
df_5 = pd.DataFrame(columns=columns)


mainDataframe(df_1, time_list_1, data_1)
mainDataframe(df_2, time_list_2, data_2)
mainDataframe(df_3, time_list_3, data_3)
mainDataframe(df_4, time_list_4, data_4)
mainDataframe(df_5, time_list_5, data_5)


# In[75]:

columns=['Time', 'InOut', 'Location1', 'Location2']

df_places_1=pd.DataFrame(columns = columns)
df_places_2=pd.DataFrame(columns = columns)
df_places_3=pd.DataFrame(columns = columns)
df_places_4=pd.DataFrame(columns = columns)
df_places_5=pd.DataFrame(columns = columns)


df_places_1['Time']=time_list_1
df_places_2['Time']=time_list_2
df_places_3['Time']=time_list_3
df_places_4['Time']=time_list_4
df_places_5['Time']=time_list_5



# In[78]:

df = [df_1, df_2, df_3, df_4, df_5]
df_places = [df_places_1,df_places_2,df_places_3,df_places_4,df_places_5]

for k in range(5):
    for i in range(len(df[k])):
        locations_list=[]
        for tag in df[k]['Tags'][i]:
            classifyLocation(tag)
        #df_places['Location'][i]=locations_list
        if len(locations_list) > 1:
            df_places[k]['Location1'][i] = locations_list[0]
            df_places[k]['Location2'][i] = locations_list[1]
        elif not locations_list:
            df_places[k]['Location1'][i] = None
            df_places[k]['Location2'][i] = None
        else:
            df_places[k]['Location1'][i] = locations_list[0]
            df_places[k]['Location2'][i] = None


# In[97]:

def splitTime(time_list, df_places):
    hour = []
    min = []
    sec = []

    for time in time_list:
        hour.append(time[0:2])
        min.append(time[2:4])
        sec.append(time[4:6])
    df_places['Hour'] = hour
    df_places['Minute'] = min
    df_places['Second'] = sec


# In[98]:

time_list = [time_list_1,time_list_2,time_list_3,time_list_4,time_list_5]

for k in range(5):
    splitTime(time_list[k], df_places[k])


# In[105]:

writer = pd.ExcelWriter('df_places_updated_5.xlsx')
df_places_5.to_excel(writer,'Sheet1')
writer.save()


# In[162]:

unique_hour = []
for i in range(5):
    unique_hour.append(sorted(set(df_places[i]['Hour'])))
    
print(unique_hour)
print(len(unique_hour))


# In[171]:

columns = ['Day', 'Hour', 'Indoor Count', 'Outdoor Count']
df_hr1 = pd.DataFrame(columns=columns)
df_hr2 = pd.DataFrame(columns=columns)
df_hr3 = pd.DataFrame(columns=columns)
df_hr4 = pd.DataFrame(columns=columns)
df_hr5 = pd.DataFrame(columns=columns)

df_hour_inout = [df_hr1, df_hr2, df_hr3, df_hr4, df_hr5]

for k in range(5):
    for j in range(len(unique_hour[k])):
        indoorcount=0
        outdoorcount=0
        for i in range(len(df_places[k])):
            if df_places[k]['Hour'][i] == unique_hour[k][j]:
                if df_places[k]['InOut'][i] == 'indoor':
                    indoorcount+=1
                elif df_places[k]['InOut'][i] == 'outdoor':
                    outdoorcount+=1
        df_hour_inout[k].loc[j] = [ k+1,unique_hour[k][j], indoorcount, outdoorcount]


# In[179]:

df_hour_all = df_hour_inout[0].append(df_hour_inout[1].append(df_hour_inout[2].append(df_hour_inout[3].append(df_hour_inout[4] ,ignore_index=True) ,ignore_index=True) ,ignore_index=True) ,ignore_index=True)


# In[181]:

writer = pd.ExcelWriter('df_hour_inout.xlsx')
df_hour_all.to_excel(writer,'Sheet1')
writer.save()


# In[144]:

totaldf_places = df_places_1.append(df_places_2.append(df_places_3.append(df_places_4.append(df_places_5, ignore_index=True), ignore_index=True), ignore_index=True), ignore_index=True)


# In[146]:

writer = pd.ExcelWriter('totaldf_places.xlsx')
totaldf_places.to_excel(writer,'Sheet1')
writer.save()


# In[190]:

df = pd.DataFrame(columns = ['Day', 'Hour', 'Concept'])

def checkConcept():
    if df_hour_all['Indoor Count'] > df_hour_all['Outdoor Count']:
        concept = 'indoor'
    else:
        concept = 'outdoor'        

        
conceptlist = []

for j in range(len(df_hour_all)):
    if df_hour_all['Indoor Count'][j] >= df_hour_all['Outdoor Count'][j]:
        concept = 'indoor'
    else:
        concept = 'outdoor'
    conceptlist.append(concept)
                
        

# In[192]:

df_hour_all['Concept'] = conceptlist

