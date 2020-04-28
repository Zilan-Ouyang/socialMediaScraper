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

def scroll(driver, timeout):
    scroll_pause_time = timeout
    count = 0
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        #if count == 20
            #scroll_pause_time = scroll_pause_time + 5
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
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    scroll(driver, 10) # scrolls the page 
    #some nasty code here to scrape the posts from company page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup_content = soup.text.strip()
    feed_div = soup.find('div', {'class': '_1xnd'}) #class="occludable-update ember-view"
    length = len(feed_div)
    print(length)
    count = 0
    data_frame = []
    data_frame.append(['Date', 'Content', 'Images', 'Video', 'Likes', 'Comments', 'Shares'])
    if feed_div != -1 :
        for posts in feed_div:
            each_page = posts.find_all('div', {'class':'_4-u2 _4-u8'})
            if each_page != -1:
                for post in each_page:
                    print('this is {}'.format(count))
                    if not len(post):
                        continue
                    if isinstance(post, element.NavigableString):
                        continue
                    post_date = post.find('span',{'class': 'timestampContent'})
                    if hasattr(post_date, 'text'):
                        post_date_text = post_date.text
                    else:
                        continue
                    print(post_date_text)
                    #print(post_date_text)
                    post_content = post.find('div', {'class':'_5pbx userContent _3576'}) 
                    if post_content is not None:
                    #if post_content != -1:
                        post_content_text = post_content.text
                        print(post_content_text)
                    else:
                        post_content_text = ''
                    print(post_content)
                    post_images = post.find_all('div', {'class':'uiScaledImageContainer'})
                    image_array = []
                    #print(post_images)
                    if len(post_images) > 0:
                        for image in post_images:
                            pic_src = image.find('img',{"src":True})
                            image_array.append(pic_src['src'])
                        print(image_array)
                    #post_images_text = post_images.text.strip()
                    post_video = post.find('video',{"src":True})
                    print(post_video)
                    if post_video is not None:
                        video = post_video['src']
                        print(video)
                    else: 
                        video = post_video
                    #post_video_text = post_video.text.strip()
                    post_likes = post.find('span', {'class':'_3dlh _3dli'})
                    print(post_likes)
                    if post_likes is not None:
                        post_likes_text = post_likes.text
                        print(post_likes_text)
                    else:
                        post_likes_text = '0'
                    #if hasattr(post_likes, 'text'):
                        #post_likes_text = post_likes.text
                        #print(post_likes_text)
                    #else:
                        #post_likes_text = '\n'
                    post_comments = post.find('a', {'class':'_3hg- _42ft'})
                    print(post_comments)
                    if post_comments is not None:
                        post_comments_text = post_comments.text
                        print(post_comments_text)
                    else:
                        post_comments_text = '0'
                    #if hasattr(post_comments, 'text'):
                        #post_comments_text = post_comments.text
                        #print(post_comments_text)
                    #else: 
                        #post_comments_text = '\n'
                    post_shares = post.find('a', {'class': '_3rwx _42ft'})
                    print(post_shares)
                    if post_shares is not None:
                        post_shares_text = post_shares.text
                        print(post_shares_text)
                    else: 
                        post_shares_text = '0'
                    row = [post_date_text, post_content_text, image_array, video, post_likes_text, post_comments_text.strip('\n'), post_shares_text.strip('\n')]
                    data_frame.append(row)
                    #post_content = post.text.strip()#.find('div', {'class': 'feed-shared-text relative feed-shared-update-v2__commentary  ember-view'})
                    count = count + 1
        #print(data_frame)
        #filtering out duplicated rows
        #df = np.array(data_frame)
        #b = np.ascontiguousarray(df).view(np.dtype((np.void, df.dtype.itemsize * df.shape[1])))
        #_, idx = np.unique(b, return_index=True)
        #unique_df = df[idx]
        with open('Facebook_{}.csv'.format(company), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data_frame)
    #company_posts = [[post.post_date_text, post.post_content_text, post.post_images,post.post_video,post.post_likes_text,post.post_comments_text] for post in feed_div]

def batchScrapping(Array):
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    driver = webdriver.Chrome('/Users/zilanouyang/downloads/chromedriver',options=options)
    # define linkedin username and password here
    email = "login email"
    password = "login password"
    #login 
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    email_elem = driver.find_element_by_id("email")
    email_elem.send_keys(email)
    password_elem = driver.find_element_by_id("pass")
    password_elem.send_keys(password)
    driver.find_element_by_id("loginbutton").click()
    #YOU HAVE TO FINISH CAPTCHA IN 60S, or you could extend it
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "pinnedNav")))
    n = len(Array)
    for i in range(n): 
        print(Array[i])
        facebook_scraper(Array[i], driver)
        
    driver.quit()


#linked_scraper('shell')

Array = [				
    'HondaCanada'	,	
    'officialsaicmotormg'	,		
    'ford'
]
batchScrapping(Array)