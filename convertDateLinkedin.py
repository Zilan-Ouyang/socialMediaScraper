import numpy as np
import pandas as pd
from datetime import datetime
#import dateutil.relativedelta

def readingFile(Filename): #Linkedin Data/Linkedin_american-honda-motor-company-inc-.csv
    data = pd.read_csv('./Linkedin_Data/Linkedin_{}.csv'.format(Filename))
    print (data['Date'])
    currentDate = datetime.strptime("2020-04-23", "%Y-%m-%d")
    for index, row in data.iterrows():
        if 'days ago' in row['Date'] or 'day ago' in row['Date']:
            res = [int(i) for i in row['Date'].split() if i.isdigit()]
            postDate = currentDate - pd.DateOffset(days= res[0])
            data.iloc[index, data.columns.get_loc('Date')] = postDate.date()
            #print(data['Date'])
            #print (postDate.date())
        elif 'weeks ago' in row['Date'] or 'week ago' in row['Date']:
            res = [int(i) for i in row['Date'].split() if i.isdigit()]
            postDate = currentDate - pd.DateOffset(weeks= res[0])
            #row['Date']= postDate
            data.iloc[index, data.columns.get_loc('Date')] = postDate.date()
            #print (postDate.date())
        elif 'months ago' in row['Date'] or 'month ago' in row['Date']:
            res = [int(i) for i in row['Date'].split() if i.isdigit()]
            postDate = currentDate - pd.DateOffset(months= res[0])
            #row['Date']= postDate
            data.iloc[index, data.columns.get_loc('Date')] = postDate.date()
            #print (postDate.date())
        else:
            res = [int(i) for i in row['Date'].split() if i.isdigit()]
            postDate = currentDate - pd.DateOffset(years= res[0])
            #row['Date']= postDate
            data.iloc[index, data.columns.get_loc('Date')] = postDate.date()
            #print (postDate.date())
    print(data)
    data.to_csv('./Linkedin_Data/Linkedin_{}.csv'.format(Filename),index=False)

def batchRename(Array):
    n = len(Array)
    for i in range(n):
        print(Array[i])
        readingFile(Array[i])

Array = [				
    'chongqing-changan'
]

batchRename(Array)