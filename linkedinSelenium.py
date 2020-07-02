from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from parsel import Selector
from time import sleep
from bs4 import BeautifulSoup, element
from pyquery import PyQuery
import csv

#this function is for automating infinite scrolling process
def scroll(driver, timeout):
    scroll_pause_time = timeout
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        sleep(scroll_pause_time)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height

def linkedin_scraper(company, driver):
    #open company public page
    linkedin_url = 'https://www.linkedin.com/company/{}'.format(company)
    #wait until page loaded
    driver.implicitly_wait(30)
    driver.get(linkedin_url)
    scroll(driver, 10) # scrolls the page 
    #scrape the posts from company page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup_content = soup.text.strip()
    #locate the feed container
    feed_div = soup.find('div', {'class': 'entity-all feed-container-theme ember-view'}) #class="occludable-update ember-view"
    length = len(feed_div)
    print(length)
    count = 0
    data_frame = []
    data_frame.append(['Date', 'Content', 'Images', 'Video', 'Likes', 'Comments'])
    #check if the company page has the post section, since some of the companies never posted anything on their public page
    if feed_div != -1 :
        #go through each individual post inside of the parent post container
        for post in feed_div:
            print('this is {}'.format(count))
            #check if the post has any content
            if not len(post):
                continue
            #check if the post is an ad link or not
            if isinstance(post, element.NavigableString):
                continue
            #locate the date of the post using html tag and classname
            post_date = post.find('span',{'class': 'visually-hidden'})
            #check if the post date element is empty
            if hasattr(post_date, 'text'):
                post_date_text = post_date.text
            else:
                continue
            print(post_date_text)
            #locate the post content inside of each post container using html tag and classname
            post_content = post.find('div', {'class':'feed-shared-text__text-view feed-shared-text-view white-space-pre-wrap break-words ember-view'})
            if hasattr(post_content, 'text'):
                post_content_text = post_content.text
            else:
                post_content_text = ''
            print(post_content_text)
            #get all the image sources from the post 
            post_images = post.find_all('img')
            image_array = []
            if len(post_images) > 0:
                for image in post_images:
                    image_array.append(image['src'])
                print(image_array)
            #get all the video sources from the post
            post_video = post.find_all('video')
            video = []
            if len(post_video) > 0:
                video = post_video[0]['src']
                print(video)
            #get the likes count 
            post_likes = post.find('li', {'class':'social-details-social-counts__item social-details-social-counts__reactions'})
            if hasattr(post_likes, 'text'):
                post_likes_text = post_likes.text
                print(post_likes_text)
            else:
                post_likes_text = '\n'
            #get the comments count
            post_comments = post.find('li', {'class':'social-details-social-counts__item social-details-social-counts__comments'})
            if hasattr(post_comments, 'text'):
                post_comments_text = post_comments.text
                print(post_comments_text)
            else: 
                post_comments_text = '\n'
            #insert the data into the dataframe
            row = [post_date_text, post_content_text, image_array, video, post_likes_text.strip('\n'), post_comments_text.strip('\n')]
            data_frame.append(row)
            count = count + 1
        print(data_frame)
        #write the dataframe into a csv file
        with open('Linkedin_{}.csv'.format(company), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data_frame)

def batchScraping(Array):
    driver = webdriver.Chrome('/Users/zilanouyang/downloads/chromedriver')
    # define linkedin username and password here
    email = "linkedin account info"
    password = "password"
    #login 
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    email_elem = driver.find_element_by_id("username")
    email_elem.send_keys(email)
    password_elem = driver.find_element_by_id("password")
    password_elem.send_keys(password)
    driver.find_element_by_tag_name("button").click()
    #YOU HAVE TO FINISH CAPTCHA IN 60S, or you could extend it
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "profile-nav-item")))
    n = len(Array)
    for i in range(n): 
        print(Array[i])
        linkedin_scraper(Array[i], driver)
        
    driver.quit()


#linked_scraper('shell')

Array = [																																			
    'waste-management',					
    'republic-services-inc'	
]
batchScraping(Array)