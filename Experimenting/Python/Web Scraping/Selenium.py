#This file will be used to test the selenium web scraping library

#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By

import time


#Main Method
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    #driver.get("https://www.google.com/get/videoqualityreport/")
    driver.get("https://www.youtube.com/@NBCSports")

    title = driver.find_element(By.ID, 'text')
    print(title.text)
    driver.quit()

    
    