
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


# ## Open data and obtain Time

# In[2]:

#Initialize path
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


# In[3]:

data = data_1 + data_2 + data_3 + data_4 + data_5
time_list = time_list_1 + time_list_2 + time_list_3 + time_list_4 + time_list_5


# In[6]:

columns=['Day', 'Time', 'Hour', 'Minute', 'Second', 'Detected Person', 'No of Faces', 'Age', 'Gender', 'Female Count', 'Male Count']
df_faces=pd.DataFrame(columns=columns)
df_faces['Time'] = time_list


# In[9]:

totalPersons=0
for i in range(len(df_faces)):
    malecount=0
    femalecount=0
    detectedPerson=False
    gender_perpic=[]
    age_perpic=[]
    for tag in data[i]['tags']:
        if tag['name'] == 'person':
            detectedPerson = True
            totalPersons+=1
            break
            
    no_of_faces=len(data[i]['faces'])
                    
    df_faces['No of Faces'][i] = no_of_faces
    df_faces['Detected Person'][i] = detectedPerson
    
    
        
    
    for j in range(no_of_faces):
        age_perpic.append(data[i]['faces'][j]['age'])
        gender_perpic.append(data[i]['faces'][j]['gender'])
        if data[i]['faces'][j]['gender'] == 'Male':
            malecount+=1
        elif data[i]['faces'][j]['gender'] == 'Female':
            femalecount+=1
    
    df_faces['Age'][i]=age_perpic
    df_faces['Gender'][i]=gender_perpic
    df_faces['Female Count'][i]= femalecount
    df_faces['Male Count'][i] = malecount


# In[20]:

#Calculate total time of socializing/meeting with other people
totalmeetingtime = (totalPersons*30)/60


# In[10]:

def splitTime(df):
    hour = []
    min = []
    sec = []

    for time in df['Time']:
        hour.append(time[0:2])
        min.append(time[2:4])
        sec.append(time[4:6])
    df['Hour'] = hour
    df['Minute'] = min
    df['Second'] = sec




# In[13]:

days=[]
data = [data_1, data_2, data_3, data_4, data_5]

for i in range(5):
    for j in range(len(data[i])):
        days.append(i+1)
        
df_faces['Day'] = days



# In[16]:

writer = pd.ExcelWriter('df_faces.xlsx')
df_faces.to_excel(writer,'Sheet1')
writer.save()


# ## Analysis


# In[49]:

#age group

total_day1 = 0
total_day2 = 0
total_day3 = 0
total_day4 = 0
total_day5 = 0
total_day = [total_day1,total_day2,total_day3,total_day4,total_day5]
age_count_1 = []
age_count_2 = []
age_count_3 = []
age_count_4 = []
age_count_5 = []
age_count = [age_count_1, age_count_2, age_count_3, age_count_4, age_count_5]

for k in range(5):
    total_persons=0
    age_10=0
    age_20=0
    age_30=0
    age_40=0
    age_50=0
    age_60=0
    age_70=0
    age_80=0
    age_90=0
    for i in range(len(df_faces)):
        if df_faces['Day'][i] == k+1:
            if len(df_faces['Age'][i]) > 0:
                for j in range(len(df_faces['Age'][i])):
                    if df_faces['Age'][i][j]<11:
                        age_10 = age_10 + 1
                    elif df_faces['Age'][i][j] < 21:
                        age_20 = age_20 + 1
                    elif df_faces['Age'][i][j] < 31:
                        age_30 = age_30 + 1
                    elif df_faces['Age'][i][j] < 41:
                        age_40 = age_40 + 1
                    elif df_faces['Age'][i][j] < 51:
                        age_50 = age_50 + 1
                    elif df_faces['Age'][i][j] < 61:
                        age_60 = age_60 + 1
                    elif df_faces['Age'][i][j] < 71:
                        age_70 = age_70 + 1
                    elif df_faces['Age'][i][j] < 81:
                        age_80 = age_80 + 1
                    else:
                        age_90 = age_90 + 1

            total_persons += df_faces['No of Faces'][i]
    total_day[k] = total_persons
    age_count[k]= [age_10, age_20, age_30, age_40, age_50, age_60, age_70, age_80, age_90]
    


# In[55]:

Day_1 = age_count[0]
Day_2 = age_count[1]
Day_3 = age_count[2]
Day_4 = age_count[3]
Day_5 = age_count[4]


# In[65]:

Age_Group = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90']
columns = ['Age_Group', 'Day_1', 'Day_2', 'Day_3', 'Day_4', 'Day_5']
df_agegroup = pd.DataFrame(columns=columns)
df_agegroup['Age_Group'] = Age_Group
df_agegroup['Day_1'] = Day_1
df_agegroup['Day_2'] = Day_2
df_agegroup['Day_3'] = Day_3
df_agegroup['Day_4'] = Day_4
df_agegroup['Day_5'] = Day_5


# In[67]:

writer = pd.ExcelWriter('df_agegroup.xlsx')
df_agegroup.to_excel(writer,'Sheet1')
writer.save()


# In[81]:

df = pd.DataFrame(columns = ['Age Group', 'Day', 'Count'])

Age_Group = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90']
Age_Group = Age_Group + Age_Group + Age_Group + Age_Group + Age_Group 
days=[]
day=[]

for j in range(5):
    for i in range(9):
        day.append(j+1)
    
    
people_count = Day_1 + Day_2 + Day_3 + Day_4 + Day_5


# In[89]:

df['Age Group'] = Age_Group
df['Day']= day
df['Count'] = people_count

# In[91]:

writer = pd.ExcelWriter('df_agegroup_2.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()


# In[96]:

unique_hour = []

for i in range(5):
    hours = []
    for j in range(len(df_faces)):
        if df_faces['Day'][j] == i+1:
            hours.append(df_faces['Hour'][j])
    unique_hour.append(sorted(set(hours)))


# In[132]:

columns = ['Day', 'Hour', 'Face Detected']
df_1 = pd.DataFrame(columns=columns)
df_2 = pd.DataFrame(columns=columns)
df_3 = pd.DataFrame(columns=columns)
df_4 = pd.DataFrame(columns=columns)
df_5 = pd.DataFrame(columns=columns)

df_hour_faces = [df_1, df_2, df_3, df_4, df_5]

for k in range(5):   
    for j in range(len(unique_hour[k])):  
        detectedFace = 0
        for i in range(len(df_faces)):
            if df_faces['Hour'][i] == unique_hour[k][j] and df_faces['Day'][i] == k+1:
                if df_faces['No of Faces'][i] > 0:
                    detectedFace+=1 
        df_hour_faces[k].loc[j] = [k+1,unique_hour[k][j], detectedFace]


# In[136]:

df_hour_faces = df_1.append(df_2.append(df_3.append(df_4.append(df_5, ignore_index=True), ignore_index=True), ignore_index=True), ignore_index=True)


# In[138]:

writer = pd.ExcelWriter('df_hour_faces.xlsx')
df_hour_faces.to_excel(writer,'Sheet1')
writer.save()
