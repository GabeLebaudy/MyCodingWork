#This file will be used to scrape the general internet connectivity data from google about different providers. 


#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from SQL_Connection import ServerConnection
from vpn import DynamicIP
from PIL import Image
from datetime import datetime
import time, sys, os, re, random

#Constants
from logger import LOG

#Get the website driver object, and the object for controlling the mouse positioning
def prepWebsite():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com/get/videoqualityreport/")
    driver.maximize_window()

    #Create Action Chains object for moving the mouse to specific spots on the screen
    mouse_controller = ActionChains(driver)
    
    return driver, mouse_controller

#This is the function that should get called once every 7 days, or whatever time period chosen to select all the data
def main_data_method():
    #TODO: Send a call to the scheduler to call this function again in 7 days time

    #Initialize SQL Connection and the IP protection
    LOG.info('Starting up SQL and IP Connections...')
    sql_cxn = ServerConnection()
    ip_ctrl = DynamicIP()

    #Ensure VPN is working properly
    isWorking = ip_ctrl.verifyMyIP()
    if isWorking:
        print("My IP: {}, Proxy IP: {}".format(ip_ctrl.getMyIP(), ip_ctrl.getProxyIP()))
    else:
        print("There was an error connecting to the VPN. Aborting Program.")
        sys.exit()

    #Pull data on all areas to scan and store them
    LOG.info('Getting area data...')
    states_data_path = os.path.join(os.path.dirname(__file__), 'states.txt')
    with open(states_data_path, 'r') as f:
        states = f.readline()
    
    states = states.split(',')
    random.shuffle(states)

    cities = sql_cxn.getAreaData()
    random.shuffle(cities)

    states = [] #Temporary
    
    cities = cities[:4] #Temp

    #Loop through all areas to scan until there are none left
    provider_bookmark = None #Ensure the same providers aren't scanned twice in case of mid-scan error
    while states or cities:
        driver, mouse = prepWebsite()

        #Pick a random number of areas to check before switching IP address. (For states 2-3 as they take much longer and the IP will be connected to the site for longer) (For cities 3-5)
        if states:
            iter_before_ip = random.randint(2, 3)
        else:
            iter_before_ip = random.randint(7, 10)

        #Check to see remaining amount of states or cities to scan. If there is less than the amount of iterations, use that number.
        if states:
            if len(states) < iter_before_ip:
                iter_before_ip = len(states)
        else:
            if len(cities) < iter_before_ip:
                iter_before_ip = len(cities)
            
        #For the selected amount of runs, scan each area. Then disconnect the driver, connect to a new area, and repeat until the areas data lists are empty.
        area_tried = False #Flag to signal if an area has been scanned and failed already. If so, log where the error has happend, and screenshot the page.
        for i in range(iter_before_ip):
            if states:
                current_area = states[0]
            else:
                current_area = cities[0]
            
            #TODO: 
            # For each run, start a timer thread to ensure that data is being sent back. For each step of the process, reset the timer to ensure nothing went wrong during the process.
            LOG.info('Starting scan for {}...'.format(current_area))
            data_retrieved, provider_bookmark = getInternetData(driver, mouse, current_area, sql_cxn, provider_bookmark)
            if not data_retrieved:
                if not area_tried:
                    area_tried = True
                    break
                else:
                    #Pass over the current area, grab a screenshot, then restart the IP.
                    date = datetime.today().strftime('%Y-%m-%d')

                    error_filename = os.path.join(os.path.join(os.path.dirname(__file__), 'Area Errors'), "{}_Error_{}".format(current_area, date))
                    driver.save_screenshot(error_filename)
                    
                    area_tried = False
                    if states:
                        states.pop(0)
                    else:
                        cities.pop(0)
                        
                    break
                    
            else: #Successful run
                if states:
                    states.pop(0)
                else:
                    cities.pop(0)
                
                area_tried = False
                provider_bookmark = None

        driver.quit()

        #Connect to a new area, (Not needed the first time, since verifying the IP automatically connects to a random area). Then get the driver and mouse objects
        ip_ctrl.connectToRandomArea()
        if not ip_ctrl:
            LOG.critical("Error: There was an issue with the VPN. Aborting program")
            sys.exit()
                
#Method for pulling data given the URL
def getInternetData(driver, mouse, area, sql_cxn, provider_bookmark):
    #TODO: Mess around with the time.sleep functions, see how much time can be saved by trying to lower them as much as possible
    time.sleep(1)

    #Navigate to the desired location to scan
    LOG.info('Navigating to selected area...')
    did_navigate = selectLocation(driver, mouse, area)
    if not did_navigate:
        return False, provider_bookmark

    time.sleep(0.5)

    #Get the distance between rectangle elements that when hovered over display the information about HD streams
    try:
        all_rects = driver.find_elements(By.TAG_NAME, 'rect')
        mouse_cords = processRects(all_rects)
        
        mouse_cords[1:] = findRightMovements(mouse_cords)
        mouse_cords.pop(-1)
        
        time.sleep(1)
    except:
        LOG.warning("There was an issue getting the graph rectangles.")
        return False, provider_bookmark
    
    #Find the compare providers button, and click on it
    try:
        compare_button_info_div = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='results-wrapper']/div[2]"))
        )
        class_string_contents = compare_button_info_div.get_attribute('class').split()
    except:
        LOG.warning("There was an error getting the compare providers button.")
        return False, provider_bookmark
    
    #This is to ensure the compare providers tab is not open before clicking on the button to expand it
    try:
        if len(class_string_contents) < 2:
            compare_providers_button = driver.find_element(By.CLASS_NAME, 'tab-label')
            mouse.move_to_element(compare_providers_button)
            mouse.click()
            mouse.perform()
    except:
        LOG.warning("There was an error expanding the list of providers.")
        return False, provider_bookmark
        
    time.sleep(1)

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
        pass

    #Get buttons to switch charts
    take_graph_pictures = True
    try:
        vol_chart_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='chart-toggles']/div[1]"))
        )
        per_chart_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='chart-toggles']/div[2]"))
        )
    except:
        LOG.warning("Graph toggle buttons couldn't be pulled. Graph picutures unavailable.")
        take_graph_pictures = False
    
    #Pull all buttons from HD, SD, and LD rows
    stream_definition_text = ['HD', 'SD', 'LD']
    provider_buttons = getProviderButtons(driver, provider_bookmark)
    
    error_counter = 0
    area = area.split(',')
    if len(area) < 2:
        city = None
        state = area[0].rstrip()
    else:
        city = area[0]
        state = area[1].lstrip()
    
    #Loop through all providers, Pulling all data
    for i in range(len(provider_buttons)):
        for element in provider_buttons[i]:
            #Make sure not to use hidden buttons in case of failure to press expand more
            if not element.text:
                continue
            
            try:
                mouse.move_to_element(element)
                mouse.click()
                mouse.perform()
            except:
                LOG.warning("The provider: {} could not be selected. Unable to get data".format(element.text))
                continue

            time.sleep(1)
            
            #Get percentage of streams that are HD
            graph_location, graph_size, full_data = getHighDefinitionStreams(driver, mouse, mouse_cords)
            if not graph_location:
                error_counter += 1
                if error_counter > 3:
                    #There is an issue with the current area, return False to try again.
                    LOG.warning("Too many providers for the area {} have failed. Aborting area.".format(area))
                    return False, element.text
                
                LOG.warning("There was an error getting data for the provider: {}.".format(element.text))
                continue
            
            #Get a picture of both graphs for each provider
            vol_chart_path, per_chart_path = None, None
            filename_string = "{}({}, {})".format(element.text, city, state)
            if take_graph_pictures:
                vol_chart_path, per_chart_path = getGraphImages(mouse, driver, vol_chart_button, per_chart_button, filename_string, graph_location, graph_size)
            
            #Add data to database
            sql_cxn.verifyProvider(element.text)
            sql_cxn.addFullDataEntry(city, state, element.text, stream_definition_text[i], full_data, vol_chart_path, per_chart_path)

            #Remove images from storage since they 
            if vol_chart_path:
                os.remove(vol_chart_path)
            
            if per_chart_path:
                os.remove(per_chart_path)
            
    time.sleep(1)
    
    return True, provider_bookmark

#Select location by zip code or city
def selectLocation(driver, mouse, area):
    time.sleep(0.5)

    #Get element that changes location of area data
    try:
        change_location_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='results-title ellipsize']/span[3]"))
        )
    except:
        LOG.warning("Change location element not found by scraper.")
        return False
    
    mouse.move_by_offset(100, 0)
    mouse.perform()

    time.sleep(0.5)

    #Click on the link
    try:
        mouse.move_to_element(change_location_element)
        mouse.click()
        mouse.perform()
    except:
        LOG.warning("Unable to select change location element.")
        return False
    
    time.sleep(0.5)

    #Controls for selecting a new location
    try:
        location_input_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='modal-dialog-content']/div[1]/input[1]"))
        )

        ok_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='modal-dialog-buttons']/button[1]"))
        )
    except:
        LOG.warning("Controls for navigating to new location unavailable.")
        return False

    #Type in area to the search bar
    try:
        location_input_element.send_keys(area)
    except:
        LOG.warning("Unable to type in location.")
        return False

    #Find table elements that contain names of available locations from the search
    correct_table_entry = None
    try:
        table_entrys = WebDriverWait(driver, 1).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'autocomplete-row'))
        )
        for entry in table_entrys:
            if entry.text.lower() == area.lower():
                correct_table_entry = entry

    except:
        LOG.warning("Location not available as a dropdown option.")
        return False

    time.sleep(0.5)

    try:
        mouse.move_to_element(correct_table_entry)
        mouse.click()
        mouse.perform()

        time.sleep(0.25)

        mouse.move_to_element(ok_button)
        mouse.click()
        mouse.perform()

        time.sleep(0.5)
    except:
        LOG.warning("There was an error clicking the ok button on the dialog window.")
        return False
    
    #Ensure the page navigated to a new location
    try:
        location_input_element.send_keys("test") #If the element can still receive keys, it did not go to a new page.
    except:
        return True #No errors
    
    return False

#Get all of the button elements that give provider information
def getProviderButtons(driver, provider_bookmark):
    main_storage = [
        [],
        [],
        []
    ]

    #In case the area failed, don't add buttons for areas that already failed.
    add_provider = False
    if not provider_bookmark:
        add_provider = True
    
    is_more_buttons = True
    button_num, row_id = 1, 0
    while is_more_buttons:
        try:
            xpath_string = "//div[@class='rating-rows revealed']/div[{}]/div[3]/div[1]/div[{}]".format(row_id + 3, button_num)
            element = WebDriverWait(driver, 0.5).until(
                EC.presence_of_element_located((By.XPATH, xpath_string))
            )
            
            button_num += 1
            if not add_provider:
                if element.text.lower() == provider_bookmark.lower():
                    add_provider = True
                    main_storage[row_id].append(element) 
            else:
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
        LOG.warning("There was an error getting the graph data elements. Aborting for current provider.")
        return False, False, False

    #Find the width of the svg element
    distance_to_move = (int(graph_element.get_attribute('width')) // 2) - 5

    #Move the mouse to the left side of the graph_element element
    try:
        mouse.move_to_element_with_offset(graph_element, distance_to_move * -1, 0)
        mouse.perform()
    except:
        LOG.warning("There was an error attempting to move the cursor to the graph. Aborting for current provider.")
        return False, False, False
    
    time.sleep(0.1)
    
    #Get the data
    gotData = True
    upOrDown = 1
    all_entries = []
    for movement in mouse_cords:
        mouse.move_by_offset(movement, 0)
        mouse.perform()
        time.sleep(0.1)
        gotData = processToolTipText(data_storage_element.text)
        num_trys = 1
        while not gotData:
            if num_trys >= 3:
                break
            
            mouse.move_by_offset(0, 25 * upOrDown)
            mouse.perform()
            upOrDown *= -1 
            time.sleep(0.1)
            gotData = processToolTipText(data_storage_element.text)
            num_trys += 1
        
        if not gotData:
            all_entries.append("NULL")
            continue

        if not re.search("[0-9+]", gotData[0]):
            all_entries.append("NULL")
            continue

        all_entries.append(gotData)
    
    return graph_element.location, graph_element.size, all_entries

#Process Individual Time Text
def processToolTipText(text):
    if not text:
        return False
    
    try:
        content = text.split('\n')
        hd_percentage = content[0].split(' ')[0]
        hd_percentage = hd_percentage[:-1]
    except:
        return False
    
    return hd_percentage

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
    try:
        mouse.move_to_element(per_button)
        mouse.click()
        mouse.perform()
    except:
        LOG.warning("There was an error moving to the graph toggle button. Pictures won't be saved.")
        return None, None
    
    time.sleep(0.75)

    driver.save_screenshot(per_chart)

    #Reset to volume chart
    try:
        mouse.move_to_element(vol_button)
        mouse.click()
        mouse.perform()
    except:
        LOG.warning("There was an error re-selecting the volume chart. Aborting for area.")
        return None, None
    
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

    return vol_chart, per_chart

#Main Method
if __name__ == "__main__":
    main_data_method()

    