

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


import io, urllib
import os 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\ImageAssignment-2f16f129fb67.json"



if __name__ == '__main__':
    # URL of the page
    PAGE_URL = "https://www.amazon.com/Harman-Kardon-Wireless-Bluetooth-Speaker/dp/B074P79X9C/ref=sr_1_1?s=amazon-devices&ie=UTF8&qid=1514002097&sr=8-1&keywords=Harman+Kardon"
    # path to the chrome driver
    CHROME_PATH = "C:/Users/baruaa/downloads/chromedriver"

    # POST_LOADS is the number of pages to get reviews from a single product; manually update to number less than total # of page reviews available
    POST_LOADS = 8
    LOAD_PAUSE_TIME = 2
    PAGE_LOAD_TIME = 2

    # RETRIEVING THE URL
    driver = webdriver.Chrome(executable_path= CHROME_PATH)
    driver.get(PAGE_URL)

    #manually set # reviews here, change this number based on what you are scraping 
    driver.find_element_by_xpath("//*[contains(text(), 'See all 73 reviews')]").click()



    # obtain the links of all the posts using 'customer-reviews' attribute
    #links stores a WebElement object type
    i = 0
    urls = []
    while i < POST_LOADS: 
        links = driver.find_elements_by_xpath("//a[contains(@data-hook, 'review-title')]")
        #converts each link to type string and appends it to url array
        for each in links:
            reviewlink = each.get_attribute("href")
            url = reviewlink.strip()
            asciistring = url.encode("ascii")
            urls.append(asciistring) 
       
        driver.find_element_by_xpath("//a[contains(text(),'Next')]").click() 

        i += 1 
        time.sleep(PAGE_LOAD_TIME)


    
    #creating an empty data frame for amazon reviews 
    amazon_reviews = pd.DataFrame(columns= ['review_id','user_name', 'review_title', 'review_rating', 'user_comment', 'review_link'])



    #loop to open each customer review individually and extract needed data 
    for link_id in range(0, len(urls)):
        link = urls[link_id]
        #driver.refresh()
        time.sleep(PAGE_LOAD_TIME)

        #throws an stale reference exception 
        #reviewlink = link.get_attribute("href")
        #actualurl = reviewlink
        
        # opening the link in a new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
 

        driver.get(link) 
        driver.get(element.get_attribute("href"))
        time.sleep(PAGE_LOAD_TIME)

        #intializing the values
        #review_rating = ""
        review_text = ""
        user_name = ""

        
        # retrieving user review 
        review_text = driver.find_element_by_xpath("//*[contains(@data-hook, 'review-body')]").text
             
        # retrieving user name
        user_name = driver.find_element_by_xpath("//a[contains(@data-hook, 'review-author')]").text

        # retrieving review rating
        #review_rating_elem = driver.find_element_by_xpath("//i[contains(@data-hook, 'review-star-rating')]")
        #review_rating = review_rating_elem.find_element_by_tag_name('span').text

        # retrieving comment title
        review_title =  driver.find_element_by_xpath("//a[contains(@data-hook, 'review-title')]").text
    
        #print it in the data fram
        amazon_reviews.loc[len(amazon_reviews)] = [link_id, user_name, review_title, review_text, reviewlink]

        print "review #: " + str(link_id) + "- "+ str(len(amazon_reviews))
        driver.close()
        #switching back to the initial tab
        driver.switch_to.window(driver.window_handles[0])
    driver.close()
    # writing the excel files
    # copy datafram to excel file 
    amazon_reviews.to_excel('speaker_user_reviews.xlsx', index = False)
    





