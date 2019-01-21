
# coding: utf-8

# In[2]:

import pandas as pd
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
import http.client, urllib.request, urllib.parse, urllib.error


# In[88]:

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


# In[105]:

data_list = data_1 + data_2 + data_3 + data_4 + data_5
time_list = time_list_1 + time_list_2 + time_list_3 + time_list_4 + time_list_5


# In[93]:

columns=['Day', 'Time', 'Hour', 'Minute', 'Second', 'Activity']
df_activity=pd.DataFrame(columns=columns)
df_activity['Time'] = time_list


# In[95]:

#Filename of images represent the time the images were taken
#splitTime(df) is to take the name of the files and record in pandas dataframe as the time for each image
def splitTime(df):
    hour = []
    min = []
    sec = []

    for time in df_activity['Time']:
        hour.append(time[0:2])
        min.append(time[2:4])
        sec.append(time[4:6])
    df['Hour'] = hour
    df['Minute'] = min
    df['Second'] = sec


# In[96]:

splitTime(df_activity)


# In[99]:

days=[]
data = [data_1, data_2, data_3, data_4, data_5]

for i in range(5):
    for j in range(len(data[i])):
        days.append(i+1)
        
df_activity['Day'] = days


# In[3]:

columns=['Time', 'Tags']

df_1=pd.DataFrame(columns=columns)

for i in range(len(time_list_1)):
    try:
        df_1.loc[i] = [time_list_1[i], data_1[i]['tags']]
    except:
        df_1.loc[i]= [time_list_1[i], 'null']

# In[5]:

consumingcount=0
act_file=['browsing_shop', 'commuting', 'using_computer', 'using_phone', 'attend_conference', 'eating', 'drinking', 'being_outside', 'attend_socialevent', 'socializing', 'sports', 'working']
count={'browsing_shop':0, 'commuting':0, 'using_computer':0, 'using_phone':0, 'attend_conference':0, 'eating':0, 'drinking':0, 'being_outside':0, 'attend_socialevent':0, 'socializing':0, 'sports':0, 'working':0}


for i in range(len(act_file)):
    with open(act_file[i] + '.txt', "r+") as file:
        WFA = file.read().split('\n')
        for tag in tags:
            if tag in WFA:
                count[act_file[i]]+=1


            




# In[103]:

morethan3 = ['being_outside', 'sports', 'working']
morethan2 = ['commuting', 'using_computer', 'using_phone', 'attend_conference', 'attend_socialevent']
morethan1 = ['browsing_shop', 'socializing', 'eating', 'drinking']
activity = []

for key, value in count.items():
    #print(key,':', value)
    if key in morethan3 and value>=3:
        activity.append(key)
    elif key in morethan2 and value>=2:
        activity.append(key)
    elif key in morethan1 and value>=1:
        activity.append(key)



# In[41]:

columns=['Time', 'Activity']

df_activity_2=pd.DataFrame(columns=columns)
df_activity_2['Time'] = time_list_1


# ## 1) Loop through tag names and hints
# In[48]:

with open('nonactivity.txt', "r+") as file:
        nonactivity = file.read().split('\n')
        
activity = []


for tags in df_1['Tags']:
    activities_tags = []
    for tag in tags:
        if tag['name'] not in nonactivity :
            result=nltk.tag.pos_tag([tag['name']])
            if result[0][1].startswith("VB"):
                activities_tags.append(tag['name'])
                
    if activities_tags:
        activity.append(activities_tags)
    else:
        count={'browsing_shop':0, 'commuting':0, 'using_computer':0, 'using_phone':0, 'attend_conference':0, 
               'eating':0, 'drinking':0, 'being_outside':0, 'attend_socialevent':0, 'socializing':0, 'sports':0, 'working':0}
        for act in act_file:
            with open(act + '.txt', "r+") as file:
                WFA = file.read().split('\n')
                for tag in tags:
                    if tag['name'] in WFA:
                        count[act]+=1
        
        for key, value in count.items():
            if key in morethan3 and value>=3:
                activities_tags.append(key)
            elif key in morethan2 and value>=2:
                activities_tags.append(key)
            elif key in morethan1 and value>=1:
                activities_tags.append(key)
        activity.append(activities_tags)
        


# In[50]:

df_activity['Activity'] = activity


# In[65]:

df_activity_first = df_activity.drop('Activity_2', 1)

# In[43]:

for i in range(len(data_1)):
    activity_list=[]
    for tag in data_1[i]['description']['tags']:
        #print(tag)
        result=nltk.tag.pos_tag([tag])
        if result[0][1] == 'VBG':
            activity_list.append(tag)
    df_activity_2['Activity'][i] = activity_list


# In[60]:

des_tags_activity = df_activity_2['Activity']


# In[81]:

from datetime import time, tzinfo, timedelta

time_list_new = []
for t in time_list_1:
    #t = time(int(t[0:2]), int(t[2:4]), int(t[4:6]))
    t = t[0:2] + ':' + t[2:4] + ':' + t[4:6]
    time_list_new.append(t)
    
print(time_list_new[0])


# In[82]:

df_activity_first['Time'] = time_list_new


# In[84]:

writer = pd.ExcelWriter('df_activity_first.xlsx')
df_activity_first.to_excel(writer,'Sheet1')
writer.save()


# In[104]:

data = data_1 + data_2 +data_3 + data_4 + data_5


# In[112]:

#improvised

with open('nonactivity.txt', "r+") as file:
        nonactivity = file.read().split('\n')
        
activity = []


for i in range(5):
    activities_tags = []
    for j in range(len(data[i])):
        for tag in data[i][j]['tags']:
            if tag['name'] not in nonactivity:
                result=nltk.tag.pos_tag([tag['name']])
                if result[0][1] == ("VBG"):
                    activities_tags.append(tag['name'])

        for tag in des_tags_activity:
            if tag not in nonactivity:
                activities_tags.append(tag)    
                
        if activities_tags:
            activity.append(activities_tags)
        else:
            count={'browsing_shop':0, 'commuting':0, 'using_computer':0, 'using_phone':0, 'attend_conference':0, 
                   'eating':0, 'drinking':0, 'being_outside':0, 'attend_socialevent':0, 'socializing':0, 'sports':0, 'working':0}
            for act in act_file:
                with open(act + '.txt', "r+") as file:
                    WFA = file.read().split('\n')
                    for tag in tags:
                        if tag['name'] in WFA:
                            count[act]+=1

            for key, value in count.items():
                if key in morethan3 and value>=3:
                    activities_tags.append(key)
                elif key in morethan2 and value>=2:
                    activities_tags.append(key)
                elif key in morethan1 and value>=1:
                    activities_tags.append(key)
            activity.append(activities_tags)
        



# In[142]:

with open('nonactivity.txt', "r+") as file:
        nonactivity = file.read().split('\n')
        
activities = []

for i in range(len(data)):
    
    for j in range(len(data[i])):
        for tag in data[i][j]['description']['tags']:
            if tag not in nonactivity:
                result=nltk.tag.pos_tag([tag])
                if result[0][1] == ("VBG"):
                    activity = tag
                    
        if activity:
            activities.append(activity)
        else:
            for tag in data[i][j]['tags']:
                if tag['name'] not in nonactivity:
                    result=nltk.tag.pos_tag([tag['name']])
                    if result[0][1] == ("VBG"):
                        activity = tag['name']
        
            if activity:
                activities.append(activity)
            else:
                #act_file/morethan123 already defined kat atas
                count={'browsing_shop':0, 'commuting':0, 'using_computer':0, 'using_phone':0, 'attend_conference':0, 
                       'eating':0, 'drinking':0, 'being_outside':0, 'attend_socialevent':0, 'socializing':0, 'sports':0, 'working':0}
                for act in act_file:
                    with open(act + '.txt', "r+") as file:
                        WFA = file.read().split('\n')
                        for tag in data[i][j]['tags']:
                            if tag['name'] in WFA:
                                count[act]+=1

                for key, value in count.items():
                    if key in morethan3 and value>=3:
                        activity = key
                    elif key in morethan2 and value>=2:
                        activity = key
                    elif key in morethan1 and value>=1:
                        activity = key
                if activity:
                    activities.append(activity)



# In[145]:

df_activity['Activity'] = activities


# In[152]:

writer = pd.ExcelWriter('df_hour_activity.xlsx')
df_activity.to_excel(writer,'Sheet1')
writer.save()


# In[3]:

df = pd.read_excel('df_hour_activity.xlsx')


