#This file will be used to scrape the general internet connectivity data from google about different providers. 


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

#Get the website driver object, and the object for controlling the mouse positioning
def prepWebsite(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.maximize_window()

    #Create Action Chains object for moving the mouse to specific spots on the screen
    mouse_controller = ActionChains(driver)
    
    return driver, mouse_controller

#Method for pulling data given the URL
def getInternetData(url):
    driver, mouse = prepWebsite(url)

    time.sleep(1)
    
    #Get the distance between rectangle elements that when hovered over display the information about HD streams
    all_rects = driver.find_elements(By.TAG_NAME, 'rect')
    mouse_cords = processRects(all_rects)
    
    mouse_cords[1:] = findRightMovements(mouse_cords)
    mouse_cords.pop(-1)
    
    time.sleep(1)

    #Find the compare providers button, and click on it
    compare_providers_button = driver.find_element(By.CLASS_NAME, 'tab-label')
    mouse.move_to_element(compare_providers_button)
    mouse.click()
    mouse.perform()
    
    time.sleep(2)

    #Find the show more button if available for each row
    try:
        show_all_providers_elements = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'more-toggle'))
        )

        for toggle_btn in show_all_providers_elements:
            #Make sure button exists on the page before clicking on it
            if toggle_btn.text:
                mouse.move_to_element_with_offset(toggle_btn, 0, 0)
                mouse.click()
                mouse.perform()
                time.sleep(1)
            
    except:
        print("All providers are shown. No need to expand lists.")

    #Get buttons to switch charts
    try:
        vol_chart_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='chart-toggles']/div[1]"))
        )
        per_chart_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='chart-toggles']/div[2]"))
        )
    except:
        print("Toggle buttons unavailable. Pictures unable to be captured.")
        return
    
    #Pull all buttons from HD, SD, and LD rows
    stream_definition_text = ['HD', 'SD', 'LD']
    provider_buttons = getProviderButtons(driver)

    #Prep Data File
    data_output_path = os.path.join(os.path.dirname(__file__), 'DataOutput.csv')
    with open(data_output_path, 'w') as f:
        f.write("Provider,6 AM,7 AM,8 AM,9 AM,10 AM,11 AM,12 PM,1 PM,2 PM,3 PM,4 PM,5 PM,6 PM,7 PM,8 PM,9 PM,10 PM,11 PM,12 AM,1 AM,2 AM,3 AM,4 AM,5 AM\n")
    
    #Loop through all providers, Pulling all data
    for i in range(len(provider_buttons)):
        for element in provider_buttons[i]:
            #Make sure not to use hidden buttons in case of failure to press expand more
            if not element.text:
                continue

            mouse.move_to_element(element)
            mouse.click()
            mouse.perform()
            time.sleep(1)

            filename_string = "{}({})".format(element.text, stream_definition_text[i])
            #Get percentage of streams that are HD
            graph_location, graph_size, full_data = getHighDefinitionStreams(driver, mouse, mouse_cords)
            
            with open(data_output_path, 'a') as f:
                f.write("{},".format(filename_string))
                for j in range(len(full_data) - 1):
                    f.write("{},".format(full_data[j][0]))
                
                f.write("{}\n".format(full_data[-1][0]))
            
            #Get a picture of both graphs for each provider
            getGraphImages(mouse, driver, vol_chart_button, per_chart_button, filename_string, graph_location, graph_size)
        
    time.sleep(1)
    
    driver.quit()

#Get all of the button elements that give provider information
def getProviderButtons(driver):
    main_storage = [
        [],
        [],
        []
    ]

    is_more_buttons = True
    xpath_filler = ['hd row', 'sd row', 'ld row no-bottom']
    button_num, row_id = 1, 0
    while is_more_buttons:
        try:
            xpath_string = "//div[@class='{}']/div[3]/div[1]/div[{}]".format(xpath_filler[row_id], button_num)
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, xpath_string))
            )
            
            button_num += 1
            main_storage[row_id].append(element)
        except:
            button_num = 1
            row_id += 1
            if row_id > 2:
                is_more_buttons = False

    return main_storage
            
#Get the % of streams that are HD for each hour
def getHighDefinitionStreams(driver, mouse, mouse_cords):
    #Pull elements for getting streaming data
    try:
        graph_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'svg'))
        )
        data_storage_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id ='chart']/div[1]/div[3]"))
        )
    except:
        print("Error getting data elements. Aborting current provider.")
        return False

    
    #Find the width of the svg element
    distance_to_move = (int(graph_element.get_attribute('width')) // 2) - 5

    #Move the mouse to the left side of the graph_element element
    mouse.move_to_element_with_offset(graph_element, distance_to_move * -1, 0)
    mouse.perform()
    
    time.sleep(0.5)
    
    #Get the data
    gotData = True
    upOrDown = 1
    all_entries = []
    for movement in mouse_cords:
        mouse.move_by_offset(movement, 0)
        mouse.perform()
        time.sleep(0.5)
        gotData = processToolTipText(data_storage_element.text)
        num_trys = 1
        while not gotData:
            if num_trys >= 3:
                break
            
            mouse.move_by_offset(0, 10 * upOrDown)
            mouse.perform()
            upOrDown *= -1 
            time.sleep(0.1)
            gotData = processToolTipText(data_storage_element.text)
            num_trys += 1

        all_entries.append(gotData)
    
    return graph_element.location, graph_element.size, all_entries

#Process Individual Time Text
def processToolTipText(text):
    if not text:
        return False
    
    content = text.split('\n')
    hd_percentage = content[0].split(' ')[0]
    
    time_splits = content[1].split(' ')
    time_frame = "{} {}".format(time_splits[0], time_splits[1])
    
    return (hd_percentage, time_frame)

#Process which rectangles are the correct ones for mining the data
def processRects(rects):
    mouse_cords = []
    for i in range(len(rects)):
        if rects[i].get_attribute('fill') != "#cccccc":
            continue
       
        if rects[i].get_attribute('x'):
            current_cord = int(rects[i].get_attribute('x'))
            
        if len(mouse_cords) < 1:
            mouse_cords.append(current_cord)
            continue
        
        if mouse_cords[len(mouse_cords) - 2] > current_cord:
            break
        
        mouse_cords.append(current_cord)

    return mouse_cords

#Find Distance to move the mouse to the right each time for video definition data
def findRightMovements(coords):
    temp = []
    for i in range(1, len(coords)):
        temp.append(coords[i] - coords[i - 1])
        
    return temp

#Get the pictures of both graphs to later process for additional data
def getGraphImages(mouse, driver, vol_button, per_button, fileprefix, graph_loc, graph_size):
    #Generate filepaths
    vol_chart = os.path.join(os.path.join(os.path.dirname(__file__), 'Graph Pictures'), "{}_Volume_Chart.png".format(fileprefix))
    per_chart = os.path.join(os.path.join(os.path.dirname(__file__), 'Graph Pictures'), "{}_Percentage_Chart.png".format(fileprefix))
    
    #Remove if existing(Temporary)
    if os.path.exists(vol_chart):
        os.remove(vol_chart)
    
    if os.path.exists(per_chart):
        os.remove(per_chart)

    #Switch to percentage chart and save photo
    mouse.move_to_element(per_button)
    mouse.click()
    mouse.perform()

    time.sleep(0.5)

    driver.save_screenshot(per_chart)

    #Reset to volume chart
    mouse.move_to_element(vol_button)
    mouse.click()
    mouse.perform()

    #Get picture of the volume chart
    driver.save_screenshot(vol_chart)

    #Crop Images
    left, top = graph_loc['x'], graph_loc['y']
    right, bottom = left + graph_size['width'], top + graph_size['height']

    vol_image = Image.open(vol_chart)
    vol_image = vol_image.crop((left, top, right, bottom))
    vol_image.save(vol_chart)

    per_image = Image.open(per_chart)
    per_image = per_image.crop((left, top, right, bottom))
    per_image.save(per_chart)

#Main Method
if __name__ == "__main__":
    getInternetData("https://www.google.com/get/videoqualityreport/")
    
    
    
    