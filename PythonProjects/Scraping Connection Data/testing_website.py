#This file is just for testing out behavior with specific elements without having to run the entire code each time.

#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from PIL import Image
import time
import sys
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

    # try:
    #     vol_chart_button = WebDriverWait(driver, 5).until(
    #         EC.presence_of_element_located((By.XPATH, "//div[@class='chart-toggles']/div[1]"))
    #     )
    #     per_chart_button = WebDriverWait(driver, 5).until(
    #         EC.presence_of_element_located((By.XPATH, "//div[@class='chart-toggles']/div[2]"))
    #     )
    # except:
    #     print("Toggle buttons unavailable. Pictures unable to be captured.")
    #     sys.exit()
       
    # vol_chart = os.path.join(os.path.join(os.path.dirname(__file__), 'Graph Pictures'), 'Volume_Chart.png')
    # per_chart = os.path.join(os.path.join(os.path.dirname(__file__), 'Graph Pictures'), 'Percentage_Chart.png')
    
    # if os.path.exists(vol_chart):
    #     os.remove(vol_chart)
    
    # if os.path.exists(per_chart):
    #     os.remove(vol_chart)

    # driver.save_screenshot(vol_chart)

    # mouse.move_to_element(per_chart_button)
    # mouse.click()
    # mouse.perform()

    # time.sleep(0.5)

    # driver.save_screenshot(per_chart)

    # mouse.move_to_element(vol_chart_button)
    # mouse.click()
    # mouse.perform()

    # time.sleep(0.25)
    
    try:
        change_location_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='section_title']/span[1]"))
        )
        print(change_location_element.text)
    except:
        print("Element Not Found.")
    
    mouse.move_to_element(change_location_element)
    mouse.click()
    mouse.perform()
    
    time.sleep(1)
    
    driver.quit()

#Test the image crop with pillow
def testCropImage():
    image_path = os.path.join(os.path.join(os.path.dirname(__file__), 'Graph Pictures'), 'AccessMedia3(HD)_Percentage_Chart.png')
    test_image = Image.open(image_path)
    
    test_image = test_image.crop((816, 342, 816 + 465, 342 + 185))
    test_image.show()
    test_image.save(image_path)

#Main Method
if __name__ == "__main__":
    testToggleButton("https://www.google.com/get/videoqualityreport/")
    #testCropImage()