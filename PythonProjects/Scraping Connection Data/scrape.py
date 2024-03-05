#This file will be used to scrape the general internet connectivity data from google about different providers. 


#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time

#Get the website driver object, and the object for controlling the mouse positioning
def prepWebsite(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
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
        
    #Pull elements for getting streaming data
    graph_element = driver.find_element(By.TAG_NAME, 'svg') #Element to move mouse to hover over
    data_storage_element = driver.find_element(By.XPATH, "//div[@id ='chart']/div[1]/div[3]") #Div that contains the tooltip which contains the HD% Value

    #Find the compare providers button, and click on it
    compare_providers_button = driver.find_element(By.CLASS_NAME, 'tab-label')
    mouse.move_to_element(compare_providers_button)
    mouse.perform()
    mouse.click()
    
    #Find all High Definition Buttons
    getHighDefinitionStreams(mouse, graph_element, data_storage_element, mouse_cords)
    
    time.sleep(1)
    
    driver.quit()


#Get the % of streams that are HD for each hour
def getHighDefinitionStreams(mouse, graph, data_div, mouse_cords):
    #Find the width of the svg element
    distance_to_move = (int(graph.get_attribute('width')) // 2) - 5

    #Move the mouse to the left side of the graph element
    mouse.move_to_element_with_offset(graph, distance_to_move * -1, 0)
    mouse.perform()
    
    time.sleep(1)
    
    #Get the data
    gotData = True
    upOrDown = 1
    for movement in mouse_cords:
        mouse.move_by_offset(movement, 0)
        mouse.perform()
        time.sleep(1)
        gotData = processToolTipText(data_div.text)
        num_trys = 1
        while not gotData:
            if num_trys >= 3:
                break
            
            mouse.move_by_offset(0, 10 * upOrDown)
            mouse.perform()
            upOrDown *= -1 
            time.sleep(0.1)
            gotData = processToolTipText(data_div.text)
            num_trys += 1

#Process Individual Time Text
def processToolTipText(text):
    if not text:
        return False
    
    content = text.split('\n')
    hd_percentage = content[0].split(' ')[0]
    
    time_splits = content[1].split(' ')
    time_frame = "{} {}".format(time_splits[0], time_splits[1])
    
    print(hd_percentage, time_frame) 
    
    return True

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
    
#Main Method
if __name__ == "__main__":
    getInternetData("https://www.google.com/get/videoqualityreport/")
    
    
    
    