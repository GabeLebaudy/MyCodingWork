#Scrape webpage

import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, sys

def main():
    driver = webdriver.Chrome()

    driver.get("https://www.amtrak.com/")
    driver.maximize_window()

    mouse = ActionChains(driver)
    
    time.sleep(3)
    
    try:
        button_el = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler"))
        )
    except Exception as e:
        print(e)
    
    if button_el.text == "Reject All":
        mouse.move_to_element(button_el)
        mouse.click()
        mouse.perform()

    try:
        from_station_el = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "mat-input-0"))
        )
    except Exception as e:
        print("There was an issue getting input form for departure station.")
        print(e)
        driver.quit()
        sys.exit(1)

    mouse.move_to_element(from_station_el)
    mouse.click()
    mouse.perform()
    
    time.sleep(0.5)
    from_station_el.send_keys("phi")
    time.sleep(1)
    
    i = 2
    element_of_interest = None
    found = False
    while True:
        try:
            drop_down_elements = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, f"//div[@class='ng-star-inserted']/div[1]/div[{i}]"))
            )
            element_of_interest = drop_down_elements[0]
            if "phi" in element_of_interest.text.lower():
                found = True
                break 
            i += 1
        except Exception as e:
            print("Could not locate any more drop down items")
            break
    
    if element_of_interest and found: 
        mouse.move_to_element(element_of_interest)
        mouse.click()
        mouse.perform()
    elif i > 2:
        print("No dropdown item found with specified text.")
        driver.quit()
        sys.exit(1)
    else:
        print("There was an issue pulling any dropdown items")
        driver.quit()
        sys.exit(1)
        
    time.sleep(0.5)
    try:
        destination_station = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "mat-input-1"))
        )
    except Exception as e:
        print("Issue with destination station input")
        print(e)
        driver.quit()
        sys.exit(1)
    
    mouse.move_to_element(destination_station)
    mouse.click()
    mouse.perform()
    
    time.sleep(0.5)
    destination_station.send_keys("wash")
    time.sleep(1)
    
    i = 2
    element_of_interest = None
    found = False
    while True:
        try:
            drop_down_elements = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, f"//div[@class='ng-star-inserted']/div[1]/div[{i}]"))
            )
            element_of_interest = drop_down_elements[1]
            if "union" in element_of_interest.text.lower():
                found = True
                break 
            i += 1
        except Exception as e:
            print("Could not locate any more drop down items")
            break
    
    if element_of_interest and found: 
        mouse.move_to_element(element_of_interest)
        mouse.click()
        mouse.perform()
    elif i > 2:
        print("No dropdown item found with specified text.")
    else:
        print("There was an issue pulling any dropdown items")
    
    time.sleep(0.5)
    try:
        depart_date_el = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "mat-input-2"))
        )
    except Exception as e:
        print("Unable to get depart date input")
        print(e)
        driver.quit()
        sys.exit(1)
        
    mouse.move_to_element(depart_date_el)
    mouse.click()
    mouse.perform()
    
    time.sleep(1.5)

    #Text purposes
    try:
        header_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//ngb-datepicker-navigation[@class='ng-star-inserted']/div[2]"))
        )
        print(header_element.text) #Month and year
    except Exception as e:
        print(e)

    i = 2
    j = 0
    found = False
    while True:
        try:
            j += 1
            date_picker = WebDriverWait(driver, 0.5).until(
                EC.presence_of_all_elements_located((By.XPATH, f"//ngb-datepicker-month[@role='grid']/div[{i}]/div[{j}]"))
            )
            element_of_interest = date_picker[0]
            if not element_of_interest.text:
                continue

            if element_of_interest.text.strip() == "26":
                found = True
                break
            
        except Exception as e:
            print(e)
            if (j == 1 or i >= 7):
                break
            i += 1
            j = 0
    
    if i > 2 and found:
        mouse.move_to_element(element_of_interest)
        mouse.click()
        mouse.perform()

    time.sleep(0.5)

    try:
        done_button = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[@aria-label='Done']"))
        )
        print(len(done_button))
        for btn in done_button:
            if btn.text.strip() == "Done":
                mouse.move_to_element(btn)
                mouse.click()
                mouse.perform()
            else:
                print(btn.text.strip())
    except Exception as e:
        print("Couldn't find done button", e)
        driver.quit()
        sys.exit(1)

    time.sleep(1.5)

    try:
        find_trains_btn = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[@aria-label='FIND TRAINS']"))
        )
        print(len(find_trains_btn))
        for btn in find_trains_btn:
            if btn.text.strip() == "FIND TRAINS":
                mouse.move_to_element(btn)
                mouse.click()
                mouse.perform()
    except Exception as e:
        print("Couldn't get find trains button", e)
        driver.quit()
        sys.exit(1)
    
    time.sleep(4)    
    driver.quit()
    print("Lights off")

if __name__ == "__main__":
    main()