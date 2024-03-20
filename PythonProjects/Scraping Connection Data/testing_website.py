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
import re

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
    except:
        print("Element Not Found.")
        driver.quit()
        sys.exit()
    
    mouse.move_to_element(change_location_element)
    mouse.click()
    mouse.perform()
    
    time.sleep(1)

    try:
        location_input_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='modal-dialog-content']/div[1]/input[1]"))
        )

        ok_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='modal-dialog-buttons']/button[1]"))
        )
    except Exception as e:
        print(e)
        print("Input element not found")
        driver.quit()
        sys.exit()

    location_input_element.send_keys("19106")
    
    time.sleep(2)

    mouse.move_to_element(ok_button)
    mouse.double_click()
    mouse.perform()

    time.sleep(2)

    try:
        compare_providers_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'tab-label'))
        )
    except:
        print("Unable to locate compare provider button. Abandoning execution.")
        driver.quit()
    
    mouse.move_to_element(compare_providers_button)
    mouse.click()
    mouse.perform()
    
    driver.quit()

#Test the image crop with pillow
def testCropImage():
    image_path = os.path.join(os.path.join(os.path.dirname(__file__), 'Graph Pictures'), 'AccessMedia3(HD)_Percentage_Chart.png')
    test_image = Image.open(image_path)
    
    test_image = test_image.crop((816, 342, 816 + 465, 342 + 185))
    test_image.show()
    test_image.save(image_path)

#Test the regular expression to ensure a digit is within the text pulled from the tooltip
def testRegularExpression(text):
    return re.search("[0-9+][%+]", text)


#Test all states, ensure that all of them are able to be looked up in the website
def testAllStates(state):
    driver, mouse = prepWebsite("https://www.google.com/get/videoqualityreport")
    
    time.sleep(1)

    try:
        change_location_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='results-title ellipsize']/span[3]"))
        )    
    except:
        print("{} Failed. Change location element not found.".format(state))
        driver.quit()
        return
    
    mouse.move_to_element(change_location_element)
    mouse.click()
    mouse.perform()

    try:
        location_input_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='modal-dialog-content']/div[1]/input[1]"))
        )

        ok_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='modal-dialog-buttons']/button[1]"))
        )
    except:
        print("{} Failed. Location input element or ok button element not found.".format(state))
        driver.quit()
        return
    
    try:
        location_input_element.send_keys(state)
    except:
        print("{} Failed. Unable to pass state name into input element.".format(state))
        driver.quit()
        return
    
    #Find table elements that contain names of available locations from the search
    correct_table_entry = None
    try:
        table_entrys = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'autocomplete-row'))
        )
        for entry in table_entrys:
            if entry.text == state:
                correct_table_entry = entry

    except:
        print("{} Failed. State not found in list of locations. Check spelling.".format(state))
        driver.quit()
        return

    time.sleep(1)

    try:
        mouse.move_to_element(correct_table_entry)
        mouse.click()
        mouse.perform()

        time.sleep(0.25)

        mouse.move_to_element(ok_button)
        mouse.click()
        mouse.perform()
    except:
        print("{} Failed. Error redirecting to new location.".format(state))
        driver.quit()
        return

    time.sleep(1)

    driver.quit()

#Main Method
if __name__ == "__main__":
    # testToggleButton("https://www.google.com/get/videoqualityreport/")
    #testCropImage
    # print(testRegularExpression("89% 12PM"))
    # print(testRegularExpression("0%"))
    # print(testRegularExpression("100"))
    # print(testRegularExpression("--"))
    # print(testRegularExpression("seventy two"))

    
    testAllStates("Delaware")

    