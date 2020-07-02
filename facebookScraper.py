from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from parsel import Selector
from time import sleep
from bs4 import BeautifulSoup, element
from pyquery import PyQuery
import numpy as np
import csv

#this function is not in use, since facebook uses infinite scroll, sometimes the page takes awhile to load and causes timeout, this function is for imitaing human click 'load more' button for more content
def clickForMore(driver, timeout):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "www_pages_reaction_see_more_unitwww_pages_home")))
    while True:
        try:
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary btn-lg']//span[@class='glyphicon glyphicon-play']"))).click()
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, "www_pages_reaction_see_more_unitwww_pages_home"))).click()
            print("LOAD MORE RESULTS button clicked")
        except TimeoutException:
            print("No more LOAD MORE RESULTS button to be clicked")
            break
#since facebook uses infinite scroll, this function is for imitaing human scrolling down the page for more content
def scroll(driver, timeout):
    scroll_pause_time = timeout
    count = 0
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        try:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight+30);")

            # Wait to load page
            sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height
            count = count + 1
        except:
            print('Re-try.........')
            #scroll page up to certain limit
            driver.find_element_by_tag_name("body").send_keys(Keys.UP)
            sleep(5)

def facebook_scraper(company, driver):
    #open company public page
    fb_page_url = 'https://www.facebook.com/pg/{}/posts'.format(company)
    driver.implicitly_wait(30)
    driver.get(fb_page_url)
    scroll(driver, 10) # scrolls the page 
    #using beautiful soup here to scrape the posts from company page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup_content = soup.text.strip()
    #find the parent post feed container
    feed_div = soup.find('div', {'class': '_1xnd'}) 
    length = len(feed_div)
    print(length)
    count = 0
    data_frame = []
    data_frame.append(['Date', 'Content', 'Images', 'Video', 'Likes', 'Comments', 'Shares'])
    if feed_div != -1 :
        for posts in feed_div:
            #find the container contains all the posts already rendered on the page inside of the post feed container
            each_page = posts.find_all('div', {'class':'_4-u2 _4-u8'})
            if each_page != -1:
                #narrow down to each post container that only contains one post
                for post in each_page:
                    #if the post container doesn't contain anything, moving on to the next post container
                    if not len(post):
                        continue
                    #sometimes it could be an ad link randomly inserted between the posts by facebook, we are going to skip that too
                    if isinstance(post, element.NavigableString):
                        continue
                    #find the date of the post by the class name and html tag
                    post_date = post.find('span',{'class': 'timestampContent'})
                    #to ensure the span contains the date content, sometimes there could be nothing
                    if hasattr(post_date, 'text'):
                        post_date_text = post_date.text
                    else:
                        continue
                    print(post_date_text)
                    #find the post content inside of each individual post container 
                    post_content = post.find('div', {'class':'_5pbx userContent _3576'}) 
                    if post_content is not None:
                        post_content_text = post_content.text
                        print(post_content_text)
                    else:
                        post_content_text = ''
                    print(post_content)
                    #find the images content inside of each individual post container
                    post_images = post.find_all('div', {'class':'uiScaledImageContainer'})
                    image_array = []
                    #check if the post contains any images
                    if len(post_images) > 0:
                        for image in post_images:
                            #find the source of all the images 
                            pic_src = image.find('img',{"src":True})
                            image_array.append(pic_src['src'])
                        print(image_array)
                    #find if the post contains any videos
                    post_video = post.find('video',{"src":True})
                    print(post_video)
                    if post_video is not None:
                        video = post_video['src']
                        print(video)
                    else: 
                        video = post_video
                    #get all the likes count of the post 
                    post_likes = post.find('span', {'class':'_3dlh _3dli'})
                    print(post_likes)
                    #check if this post has any likes
                    if post_likes is not None:
                        post_likes_text = post_likes.text
                        print(post_likes_text)
                    else:
                        post_likes_text = '0'
                    #get all the comments count of the post
                    post_comments = post.find('a', {'class':'_3hg- _42ft'})
                    print(post_comments)
                    if post_comments is not None:
                        post_comments_text = post_comments.text
                        print(post_comments_text)
                    else:
                        post_comments_text = '0'
                    #find the shares count of the post
                    post_shares = post.find('a', {'class': '_3rwx _42ft'})
                    print(post_shares)
                    if post_shares is not None:
                        post_shares_text = post_shares.text
                        print(post_shares_text)
                    else: 
                        post_shares_text = '0'
                    #insert all the info of this specific post into the dataframe
                    row = [post_date_text, post_content_text, image_array, video, post_likes_text, post_comments_text.strip('\n'), post_shares_text.strip('\n')]
                    data_frame.append(row)
                    count = count + 1
        #after we gathered all of the post info from the account, we insert the dataframe into a csv file
        with open('Facebook_{}.csv'.format(company), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data_frame)
    
def batchScraping(Array):
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    driver = webdriver.Chrome('/Users/zilanouyang/downloads/chromedriver',options=options)
    # specify your facebook log-in username and password here
    email = "login email"
    password = "login password"
    #login process
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    email_elem = driver.find_element_by_id("email")
    email_elem.send_keys(email)
    password_elem = driver.find_element_by_id("pass")
    password_elem.send_keys(password)
    driver.find_element_by_id("loginbutton").click()
    #YOU HAVE TO FINISH CAPTCHA IN 120S, or you could extend it by changing the number
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "pinnedNav")))
    n = len(Array)
    for i in range(n): 
        print(Array[i])
        facebook_scraper(Array[i], driver)
    driver.quit()


Array = [				
    'HondaCanada'	,	
    'officialsaicmotormg'	,		
    'ford'
]
batchScraping(Array)