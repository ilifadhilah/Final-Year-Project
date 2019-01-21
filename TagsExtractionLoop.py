
# coding: utf-8
#Used Microsoft Cognitive Services API for the extraction of content from the images

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
import http.client, urllib.request, urllib.parse, urllib.error


# In[19]:

#create time list from image filenames

image_list = []
time_list = []


# In[50]:

#append time into time_list
#write folder that contains images as directory
for filename in glob.glob('C:\\Users\\User\\Documents\\FYP\\EDUB-Seg\\images\\Subject2_Set4/*.jpg'): 
    time_list.append(filename[58:64])



# In[5]:

#Cognitive Services Key and URL initialization
subscription_key = 'cffe6ad0fd944b488cc2ee49c93bd076'
uri_base = 'https://southeastasia.api.cognitive.microsoft.com/vision/v1.0'

#headers & parameters initialization
headers = {
    # Request headers.
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.parse.urlencode({
    # Request parameters. All of them are optional.
    # Categories, Tags, Description, Color, Adult, ImageType, Faces
    'visualFeatures': 'Description, Faces, Tags',
    'language': 'en',
})


# In[6]:

extracted_data=[]
for filename in glob.glob('C:\\Users\\User\\Documents\\FYP\\EDUB-Seg\\images\\Subject2_Set4/*.jpg'):
    with open(filename, 'rb') as f:
        data = f.read()
    try:
        # Execute the REST API call and get the response.
        conn = http.client.HTTPSConnection('southeastasia.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, data, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        extracted_data.append(parsed)
        conn.close()
        sleep(2)

    except Exception as e:
        print('Error:')
        print(e)


#dump data into text file
with open("ExtractedData_Subject2Set4.txt", 'w') as outfile:
    json.dump(extracted_data, outfile)


# In[11]:

#open data
with open("ExtractedData_Subject2Set2.txt", 'r') as outfile:
    data=json.load(outfile)



