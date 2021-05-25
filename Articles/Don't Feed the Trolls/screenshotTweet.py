from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import tweepy
import credentials
import sys
from PIL import Image

opts = Options()
#opts.headless = True
#assert opts.headless  # Operating in headless mode

browser = Chrome(options=opts)


# Function of waiting until the present of the element on the web page
def waiting_func(by_variable, attribute):
    try:
        WebDriverWait(browser, 10).until(lambda x: x.find_element(by=by_variable,  value=attribute))
    except (NoSuchElementException, TimeoutException):
        print('{} {} not found'.format(by_variable, attribute))
        exit()

def tweetToScreenshot(Tweeturl, message):
    # Access to Twitter
    path = []
    url = Tweeturl
    browser.get(url)
    screenImage = '_screenImage.png'
    mediaImage = '_imageoutput.png'

   
    waiting_func('id', 'react-root')
    a = browser.find_element_by_id('react-root')
    waiting_func('css selector', "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(2) > div > section > div > div > div:nth-child(1) > div > div > article > div > div")
    b = browser.find_element_by_css_selector("#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(2) > div > section > div > div > div:nth-child(1) > div > div > article > div > div")

    location = b.location
    size = b.size

    browser.save_screenshot(screenImage)
    browser.quit()

    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h

    im = Image.open(screenImage)
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(mediaImage)

    auth = tweepy.OAuthHandler(credentials.tConsumerKey, credentials.tConsumerSecret)
    auth.set_access_token(credentials.tAccessToken, credentials.tAccessTokenSecret)

    # Create API object
    api = tweepy.API(auth)

    # Create a tweet
    api.update_with_media(mediaImage, message)



if __name__ == "__main__":
   #tweetToScreenshot('https://twitter.com/anildash/status/1397197591612477450', "Stop Feeding the Trolls #SFtT")
   
   
   tweetToScreenshot(sys.argv[1], sys.argv[2])