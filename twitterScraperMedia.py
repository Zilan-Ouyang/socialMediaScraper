from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from parsel import Selector
from time import sleep
from bs4 import BeautifulSoup, element
import numpy as np
import pandas as pd
from datetime import datetime
import glob
#import dateutil.relativedelta

def readingFile(Filename, driver): #Linkedin Data/Linkedin_american-honda-motor-company-inc-.csv
    data = pd.read_csv(Filename)
    print(len(data))
    data.insert(6, "Images", '')
    data.insert(7, 'Video', '')
    #print (data['URL'])
    #currentDate = datetime.strptime("2020-04-23", "%Y-%m-%d")
    for index, row in data.iterrows():
        print(row['URL'])
        url = row['URL']
        #driver.implicitly_wait(30)
        try:
            
            driver.get(url)
            # print('here') # > div:nth-child(3)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#react-root > div > div > div.css-1dbjc4n.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-yfoy6g.r-18bvks7.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div > div > section > div > div")))
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            #print(soup)
            main = soup.find('article')
            #print(main)
            video = []
            images = []
            if main is not None:
                content = main.find_all('a')
                for a in content:
                    #print(a)
                    for img in a.find_all('img',{"src":True}):
                        if 'profile_images' not in img['src']:
                            print(img['src'])
                            images.append(img['src'])
                clip= main.find('video',{"src":True})
                print(clip)
                if clip is not None:
                    print(clip['src'])
                    video.append(clip['src'])
                print(images)
                print(video)
                print((index / len(data)) * 100)
                print(data.columns.get_loc('Images'))
                data.at[index,'Images']= images
                data.at[index,'Video'] = video
        except TimeoutException:
            driver.quit()
            options = Options()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--mute-audio")
            options.add_argument("--headless")
            driver = webdriver.Chrome('/Users/zilanouyang/downloads/chromedriver',options=options)
        #data.iloc[index, data.columns[5]] = images
        #data.iloc[index, data.columns[6]] = video
    driver.quit()
    data.to_csv(Filename,index=False)
        #content = soup.findAll('img')
        #print(content)
    """
        media = content.find_all('img')
        if media is not None or len(media)>0:
            print(media)
        break
    """

    #print(data)
    #data.to_csv('./Linkedin_Data/Linkedin_{}.csv'.format(Filename),index=False)

def batchRename(Array):
    n = len(Array)
    for i in range(n):
        """
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(executable_path=geckodriver) #, firefox_options=options)
        """
        print(Array[i])
        path = "./Twitter/{}/*.csv".format(Array[i])
        print (glob.glob(path))
        for fname in glob.glob(path):
            print(fname)
            options = Options()
            options.add_argument("--headless")  
            options.add_argument('window-size=1920x1080')
            options.add_argument("--no-sandbox")
            driver = webdriver.Chrome('/Users/zilanouyang/downloads/chromedriver',options=options)
            fname = '{filename}'.format(foldername=Array[i], filename=fname)
            readingFile(fname, driver)
        #fname = './Twitter/Toyota Motor/ToyotaEvents-all-tweets.csv'
        #fname = './Twitter/Volkswagen Group/VolkswagenAu-all-tweets.csv'
        #VW-2019-2020-tweets VWGroup-all-tweets
        #readingFile(fname, driver)

Array = [				
    #'Toyota Motor'
    #'Volkswagen Group'
    #'Honda Motor',
    'Fiat Chrysler Automobiles',
    
]

batchRename(Array)

"""
'Renault',
    'Peugeot',
    'Hyundai Motor'
Nissan Motor
Suzuki Motor
KIA Motors
Subaru
"""