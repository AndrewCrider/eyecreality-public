import time
from selenium.webdriver.common.keys import Keys
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from PIL import Image

saveLocation = '~/womboArtwork/'

def wombo(phrase, art_style, type=''):
    print(art_style)
    home_link = 'https://app.wombo.art/'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    driver.get(home_link)
    time.sleep(2)
    driver.implicitly_wait(30)
    driver.find_element_by_xpath('//*[@label="Enter prompt"]').send_keys(phrase)
    try:
        driver.find_element_by_xpath(f'//*[@alt="{art_style}"]').click()
    except:
        driver.find_element_by_xpath(f'//*[@alt="No Style"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div/div/div/div[2]/div/button').click()
    time.sleep(1)
    print("Creating the artwork")
    driver.implicitly_wait(100)
    driver.find_element_by_xpath("//input[@label='Name artwork']").click()
    
    try:
    # wait for loading element to appear
    # - required to prevent prematurely checking if element
    #   has disappeared, before it has had a chance to appear
        WebDriverWait(driver, 5
            ).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div/div/div[2]/div/div/p")))

        # then wait for the element to disappear
        WebDriverWait(driver,30
            ).until_not(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div/div/div[2]/div/div/p")))

    except TimeoutException:
    # if timeout exception was raised - it may be safe to 
    # assume loading has finished, however this may not 
    # always be the case, use with caution, otherwise handle
    # appropriately.
        pass 
    
    
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    link = soup.find_all('img')
    full_link = link[0]['src']
    print(full_link)
    img = Image.open(requests.get(full_link, stream = True).raw)
    img.save(saveLocation+type+'_'+phrase+'_'+art_style+'.jpg')

