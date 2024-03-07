#This file is just for testing out behavior with specific elements without having to run the entire code each time.

#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import os

#Helper Methods
def prepWebsite(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.maximize_window()

    #Create Action Chains object for moving the mouse to specific spots on the screen
    mouse_controller = ActionChains(driver)
    
    return driver, mouse_controller

#Test the toggle more button
def testToggleButton(url):
    driver, mouse = prepWebsite(url)

    time.sleep(2) #While the button can be located, it can't be clicked on until the animation is complete, so a small delay is needed

    #Get show providers button
    # try:
    #     compare_providers_button = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, 'tab-label'))
    #     )
    # except:
    #     print("Unable to locate compare provider button. Abandoning execution.")
    #     driver.quit()
    
    # mouse.move_to_element(compare_providers_button)
    # mouse.click()
    # mouse.perform()

    # time.sleep(2)

    picture_storage = os.path.join(os.path.join(os.path.dirname(__file__), 'Graph Pictures'), 'test_picture.png')
    if os.path.exists(picture_storage):
        os.remove(picture_storage)
    
    driver.save_screenshot(picture_storage)
    
    driver.quit()

#Main Method
if __name__ == "__main__":
    testToggleButton("https://www.google.com/get/videoqualityreport/")