#This file will be used as the main file to get the CSV file, potentially modifying it.

#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time, os
from datetime import datetime

def open_website():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.simplify.us/etfs/pink-simplify-health-care-etf")
    driver.maximize_window()

    mouse_controller = ActionChains(driver)
    
    return driver, mouse_controller

def download_data(driver, mouse):
    try:
        download_link = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='download-reports']"))
        )
    except:
        #TODO: Log HTML to file for debugging. (Potential Email Alerts)
        print("Error pulling link")
        return False
    
    time.sleep(1)

    #Click on download link
    mouse.scroll_to_element(download_link)
    mouse.scroll_by_amount(0, 100)
    mouse.perform()
    time.sleep(0.5)
    mouse.move_to_element(download_link)
    mouse.click()
    mouse.perform()

    time.sleep(1)

    try:
        date_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='holdings-table-pane']/div[1]/p[1]"))
        )
    except:
        #TODO: Log HTML to file for debugging. (Potential Email Alerts)
        print("Unable to find date of data")
        return False
    
    return date_element.text

def move_data_file(data_date):
    data_date = data_date.split(' ')[-1]
    date_obj = datetime.strptime(data_date, "%m/%d/%Y")
    formatted_date = date_obj.strftime("%Y_%m_%d")
    file_name = f"{formatted_date}_Simplify_Portfolio_EOD_Tracker.xlsx"
    #TODO: Change this to your absolute path to your downloads folder.
    downloads_folder = r"E:\Users\Gabe\Downloads"
    file_path = os.path.join(downloads_folder, file_name)
    
    #Move file if it exists.
    if os.path.exists(file_path):
        output_folder_path = r"E:\Users\Gabe\Documents\Coding Projects\MyCodingWork\PythonProjects\Stock_Data_Tracking"
        output_folder_path = os.path.join(output_folder_path, file_name)
        os.replace(file_path, output_folder_path)

def main():
    driver, mouse = open_website()

    time.sleep(1)
    data_date = download_data(driver, mouse)
    
    driver.quit()
    if not data_date:
        return False
    
    move_data_file(data_date)
    
if __name__ == "__main__":
    main()
