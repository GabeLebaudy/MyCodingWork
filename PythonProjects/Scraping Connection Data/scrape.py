#This file will be used to scrape the general internet connectivity data from google about different providers. 


#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time

#Method for pulling data given the URL
def getInternetData(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    #Create Action Chains object for moving the mouse to specific spots on the screen
    mouse_controller = ActionChains(driver)
    
    time.sleep(1)
    
    all_rects = driver.find_elements(By.TAG_NAME, 'rect')
    mouse_cords = []
    for i in range(len(all_rects)):
        if all_rects[i].get_attribute('fill') != "#cccccc":
            continue
       
        if all_rects[i].get_attribute('x'):
            current_cord = int(all_rects[i].get_attribute('x'))
            
        if len(mouse_cords) < 1:
            mouse_cords.append(current_cord)
            continue
        
        if mouse_cords[len(mouse_cords) - 2] > current_cord:
            break
        
        mouse_cords.append(current_cord)
    
    mouse_cords[1:] = findRightMovements(mouse_cords)
    
    time.sleep(1)
        
    #Element to move mouse to hover over
    graph_element = driver.find_element(By.TAG_NAME, 'svg')
    
    #Find the width of the svg element
    distance_to_move = (int(graph_element.get_attribute('width')) // 2) - 5
    
    #Div that contains the tooltip which contains the HD% Value
    div_element = driver.find_element(By.XPATH, "//div[@id ='chart']/div[1]/div[3]")
    
    mouse_controller.move_to_element_with_offset(graph_element, distance_to_move * -1, 0)
    mouse_controller.perform()
    
    time.sleep(1)
    
    gotData = True
    upOrDown = 1
    #Get the data
    for movement in mouse_cords:
        mouse_controller.move_by_offset(movement, 0)
        mouse_controller.perform()
        time.sleep(1)
        gotData = processToolTipText(div_element.text)
        num_trys = 1
        while not gotData:
            if num_trys >= 3:
                break
            
            mouse_controller.move_by_offset(0, 10 * upOrDown)
            mouse_controller.perform()
            upOrDown *= -1 
            time.sleep(0.1)
            gotData = processToolTipText(div_element.text)
            num_trys += 1
    
    time.sleep(1)
    
    driver.quit()


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
    
#Find Right Movements
def findRightMovements(coords):
    temp = []
    for i in range(1, len(coords)):
        temp.append(coords[i] - coords[i - 1])
        
    return temp
    
#Main Method
if __name__ == "__main__":
    getInternetData("https://www.google.com/get/videoqualityreport/")
    
    
    
    