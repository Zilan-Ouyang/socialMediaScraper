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
from lxml import html  
import requests
#import dateutil.relativedelta

def readingFile(Filename, driver): 
    data = pd.read_csv(Filename)
    print(len(data))
    data.insert(6, "Images", '')
    data.insert(7, 'Video', '')
    data.insert(8, 'Replies', '')
    #print (data['URL'])
    #currentDate = datetime.strptime("2020-04-23", "%Y-%m-%d")
    for index, row in data.iterrows():
        print(row['URL'])
        url = row['URL']
        tweetcontent = row['Text']
        #driver.implicitly_wait(30)
        try:
            if any(x in tweetcontent for x in ('Hi', 'hi', 'sorry', 'Sorry', 'DM')) and row['Retweets'] ==0 and row['Favorites'] ==0:
                #print (tweetcontent)
                continue
            driver.get(url)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#react-root > div > div > div.css-1dbjc4n.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-yfoy6g.r-18bvks7.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div > div > section > div > div")))
            source = driver.page_source
            soup = BeautifulSoup(source, 'lxml')
            #print(soup)
            main = soup.find('article')
            video = []
            images = []
            if main is not None:#/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/section/div/div/div[2]/div/div/div/div/article/div/div[3]/div[4]
                #print(WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div/div/section/div/div/div[1]/div/div/div/div/article/div/div[3]/div[5]"))).get_attribute("aria-label"))
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
                print(index)
                print((index / len(data)) * 100)
                #print(data.columns.get_loc('Images'))
                if len(images) == 0:
                    data.at[index,'Images']= ''
                data.at[index,'Images']= images
                if len(video) == 0:
                    data.at[index,'Video']= ''
                data.at[index,'Video'] = video
                
                try:
                    replies = WebDriverWait(driver, 0.5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div/div/section/div/div/div[1]/div/div/div/div/article/div/div[3]/div[5]")) or EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div/div/section/div/div/div[1]/div/div/div/div/article/div/div[3]/div[4]"))).get_attribute("aria-label")
                    print(replies) #css-1dbjc4n r-1oszu61 r-1gkumvb r-1efd50x r-5kkj8d r-18u37iz r-ahm1il r-a2tzq0
                    data.at[index,'Replies']= replies
                except TimeoutException:
                    continue
        except TimeoutException:
            driver.quit()
            options = Options()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--mute-audio")
            options.add_argument("--headless")
            driver = webdriver.Chrome('/Users/zilanouyang/downloads/chromedriver',options=options)
        except TypeError:
            continue
    driver.quit()
    data.to_csv(Filename,index=False)

def batchScraping(Array):
    n = len(Array)
    for i in range(n):
        #print(Array[i])
        path = "./Twitter/{}/*.csv".format(Array[i])
        #print (glob.glob(path))
        for fname in glob.glob(path):
            options = Options()
            options.add_argument("--headless")  
            options.add_argument('window-size=1920x1080')
            options.add_argument("--no-sandbox")
            driver = webdriver.Chrome('/Users/zilanouyang/downloads/chromedriver',options=options)
            fname = '{filename}'.format(foldername=Array[i], filename=fname)
            try:
                readingFile(fname, driver)
            except ValueError:
                continue

Array = [				
    'Volkswagen Group',
    'Honda Motor',
]
batchScraping(Array)
