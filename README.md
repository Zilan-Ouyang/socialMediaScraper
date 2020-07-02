# Social Media Scrappers 

This project can be used for scraping:

* Twitter （tweets, tweet media, likes count, replies count, retweets count)
* Linkedin company public page （posts, images, videos, likes count, comments count)
* Facebook company public page (posts, images, videos, likes count, comments count, shares count)

## Twitter Scrapper Usage

1. Scraping tweet contents, URL, Retweets count, Favourites count

Use the script 'twitterScraping.py', you need have the list of twitter handles you want to scrape, then put the list into the array list on the file

Here's an example:
```python
#username array consists of a list of twitter handle names
Array = ['Total', 'shell']
```

2. This script is using package 'GetOldTweets3', and since twitter has a limit on the requests, you might need to use vpn to change your IP address for every 6000 - 7000 tweets.

3. Running the script: 
```bash
python3 twitterScraping.py
```

4. Output:
the defaul output csv file name is 'twitterhandlename-all-tweets.csv'. 
You can also change the file name from this line in the script:
```python
tweets_df.to_csv('{}-all-tweets.csv'.format(username), sep=',')
```

## Twitter media scraper

Since 'GetOldTweets3' package can't get the images, videos, and replies count, therefore, this script was built for scraping the media content of the tweets that were already scraped from the twitter scraper. The file generated from the twitter scraper will be the argument used by twitter media scraper function. This script uses the tweet URL we get from the last scipt to go into that specific tweet page in order to get the media content.

1. After we get the output files from running the first twitter script, we need to specify the file path in this script:
```python
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
```
You can modify the file path in this block of codes, as long as the file path passed into 'readingFile(fname, driver)' function is the correct one, it should do the work.

2. On the first step, you will also be required to have chrome driver installed on your computer, you can also use other browser driver here depending on your preference; the chrome driver can be downloaded from here: https://chromedriver.chromium.org/
And you need to specify the location of the webdriver on your machine here:

```python
driver = webdriver.Chrome('/Users/zilanouyang/downloads/chromedriver',options=options)
```

3. Running the script:
```bash
python3 twitterScraperMedia.py
```

4. Output:
The output of this file will be inserted directly into your existed csv file.

## Facebook

Scraping facebook is different from scraping twitter, facebook would require user to have facebook credentials, and for each credential, facebook also has a limit for the requests, once you exceeded the limit, they would ask you to pass the verification captcha, therefore, on this script, the selenium and webdriver are being used, and make sure you dont set webdriver option to headless. 

### Usage
1. You also need to put a list of account names into the arrays for batch scraping. The account name can be either find in the url, like 'https://www.facebook.com/Shell', or as a handle on the page (e.g. @shell)

```python
Array = [				
    'HondaCanada',	
    'officialsaicmotormg',		
    'ford'
]
batchScraping(Array)
```
2. Set up webdriver
Make sure you disable the notifications and infobars, and specify your webdriver path on your machine
```python
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    driver = webdriver.Chrome('/Users/zilanouyang/downloads/chromedriver',options=options)
```
3. Log in with your facebook credentials. This block of code automated the log in process on facebook.
```python
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
```

4. After user logged in, the scraping process would start after webdriver spotted the side nav bar on the page; the webdriver would wait for 120 seconds maximum until the page fully loaded; if the side navbar didn't get loaded within 120s, it means either user's network is having issues or the user got blocked out by captcha, therefore, user has to complete the captcah challenge in order to let the script to have an access to facebook:
User can modify the waiting time here:
```python
WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "pinnedNav")))
```

5. Output file name can be modified here:

```python
with open('Facebook_{}.csv'.format(company), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data_frame)
```

6. Running the script:

```bash
python3 facebookScraper.py
```
## LinkedIn
For scraping LinkedIn public page, linkedin credentials are also needed.

1. The list of company account names is also required for batch scraping. You can only find the account name in the linkedin page url (e.g. https://www.linkedin.com/company/shell/, the account name would be 'shell)
```python
Array = [																	
    'waste-management',					
    'republic-services-inc'	
]
batchScraping(Array)
```

2. Set up webdriver and login credentails. The process is quite similar to facebook's, and user would also be required to do verfication captcha

3. Running the script:
```bash
python3 linkedinSelenium.py
```

4. Output file
the default out file name is 'Linkedin_{name from the array list}.csv'

5. Extra step for modifying the date of each post entry in the output csv file
After we get the output into the csv file, the date of each post would not be displayed as an actual date, instead, linkedin uses a relative date (e.g. 2 days ago).If you want to show the actual date of each post entry in your file, you can run another script in this repo called 'convertDateLinkedin.py' to convert the relative date to the actual date:
* You can keep using the array list that you used in scraping process if you didn't modify the default file name
```python
Array = [				
    'chongqing-changan'
]
```
* The script would look for the file and modify the file directly, you can modify your file path here:
```python
data = pd.read_csv('./Linkedin_Data/Linkedin_{}.csv'.format(Filename))
```
* Modify the date; for example, if you scraped the date on 4.30.2020, you can specify the current date as '2020-04-23' in the script.

```python
currentDate = datetime.strptime("2020-04-23", "%Y-%m-%d")
```
* Running the script

```python
python3 convertDateLinkedin.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

This project is only for academic and research purpose, and all the pages I scraped are public pages.
