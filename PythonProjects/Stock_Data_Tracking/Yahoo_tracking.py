#This will be the main file for the yahoo scraping.

#Imports
import requests, os, time, re, logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PyQt6.QtCore import QThread, pyqtSignal


LOGPATH = os.path.join(os.path.dirname(__file__), 'log_file.log')
LOGGER = logging.getLogger('Main Logger')
LOGGER.setLevel(logging.INFO)
output = logging.FileHandler(LOGPATH, 'w')
formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s - %(asctime)s', 'on %m/%d/%Y at %H:%M %p')
output.setFormatter(formatter)

LOGGER.addHandler(output)

# cookie_names = ['GUC', 'A1', 'A3', 'A1S', 'DSS', 'PRF', 'gpp', 'gpp_sid', 'cmp', '_charbeat2', '_cb_svref', '_SUPERFLY_lockout=1']

class Scraper(QThread):
    response_code_signal = pyqtSignal(int)
    info_response_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.stock_abbr = None
        self.output_path = None
        
    def setStockAbbr(self, abbr):
        self.stock_abbr = abbr
        
    def setOutputPath(self, path):
        self.output_path = path
    
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=options)
        driver.get("https://finance.yahoo.com/")
        driver.maximize_window()
        
        mouse = ActionChains(driver)
        
        return driver, mouse

    def getStockReqInfo(self):
        LOGGER.info("Starting scrape with for {}".format(self.stock_abbr))
        driver, mouse = self.setup_driver()

        time.sleep(1)
        #Search bar element
        try:
            search_bar_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "ybar-sbq"))
            )    
        except:
            LOGGER.error("Issue with the search bar element.")
            self.response_code_signal.emit(1)
            driver.quit()
            return False
        
        search_bar_element.send_keys(self.stock_abbr)
        time.sleep(1)

        #Find list of options from search
        found = False
        c = 0
        while not found:
            c += 1
            try:
                list_option_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//ul[@role='listbox']/li[{}]/div[1]/div[1]/div[1]".format(c)))
                )
                if self.stock_abbr == list_option_element.text:
                    found = True
            except:
                break

        if not found:
            LOGGER.warning("Could not find stock with given abbreviation {}".format(self.stock_abbr))
            self.response_code_signal.emit(2)
            driver.quit()
            return False

        mouse.move_to_element(list_option_element)
        mouse.click()
        mouse.perform()
        time.sleep(2)

        #Click on historical data
        found = False
        c = 0
        while not found:
            c += 1
            try:
                bar_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//ul[@role='menubar']/li[{}]".format(c)))
                )
                if bar_element.text == "Historical Data":
                    found = True
            except:
                break

        if not found:
            LOGGER.error("Issue finding the 'historical data' option.")
            self.response_code_signal.emit(3)
            driver.quit()
            return False

        mouse.move_to_element(bar_element)
        mouse.click()
        mouse.perform()
        time.sleep(2)

        #Click on max amount of data available, to find correct URL
        try:
            button_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='history-table']/div[1]/div[1]/buttn[1]"))
            )
        except:
            LOGGER.error("Could not find date selection button.")
            self.response_code_signal.emit(4)
            driver.quit()
            return False
        
        mouse.move_to_element(button_element)
        mouse.click()
        mouse.perform()
        time.sleep(1)
        
        found = False
        c = 0
        while not found:
            c += 1
            try:
                max_button = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='document']/section[1]/div[1]/button[{}]".format(c)))
                )
                if max_button.text == "Max":
                    found = True
            except:
                break
        
        if not found:
            LOGGER.error("Could not find max button to find all available info for {}".format(self.stock_abbr))
            self.response_code_signal.emit(5)
            driver.quit()
            return False
        
        mouse.move_to_element(max_button)
        mouse.click()
        mouse.perform()
        time.sleep(2)

        url = driver.current_url
        cookies = driver.get_cookies()

        time.sleep(1)
        driver.quit()
        return (url, cookies)

    def getJsonData(self, site_info):    
        #Generate cookie string
        url, cookies = site_info[0], site_info[1]
        cookie_str = ""
        for cookie in cookies:
            if cookie['value'] != 'null':
                cookie_str += cookie['name'] + '=' + cookie['value'] + '; '

        cookie_str.rstrip()
        url_items = url.split('/')
        abbr = url_items[4]
        time_period_str = url_items[-1]
        period_1 = re.search(r'period1=\d+', time_period_str).group().split('=')[1]
        period_2 = re.search(r'period2=\d+', time_period_str).group().split('=')[1]
        url = "https://query1.finance.yahoo.com/v8/finance/chart/{}".format(abbr)
        
        querystring = {"events":"capitalGain|div|split","formatted":"true","includeAdjustedClose":"true",
                    "interval":"1d","period1":period_1,"period2":period_2,"symbol":abbr,"userYfid":"true","lang":"en-US","region":"US"}

        payload = ""
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cookie": cookie_str,
            "origin": "https://finance.yahoo.com",
            "priority": "u=1, i",
            "referer": url,
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        
        #Log all info for the request
        LOGGER.info(url)
        LOGGER.info("Headers %s", headers)
        LOGGER.info("Query string %s", querystring)
        try:
            response = requests.request("GET", url, data=payload, headers=headers, params=querystring).json()
        except Exception as e:
            LOGGER.error("%s", e)
            return False
        
        return response

    def parseJsonData(self, response):
        main_data = response["chart"]["result"][0]
        stock_timestamps = main_data["timestamp"]
        stock_data = main_data["indicators"]["quote"][0]
        adjClose = main_data["indicators"]["adjclose"][0]["adjclose"]
        has_dividends = True
        try:
            dividends_dict = main_data["events"]["dividends"]
        except:
            has_dividends = False

        num_items = len(stock_timestamps)
        output_path = os.path.join(os.path.dirname(__file__), "{}_main_data.csv".format(self.stock_abbr))
        with open(output_path, 'w') as f:
            f.write("Date,Open,High,Low,Close,Adj Close,Volume\n")
            
            for i in range(num_items):
                f.write("{},{},{},{},{},{},{}\n".format(datetime.fromtimestamp(stock_timestamps[i]).strftime("%Y-%m-%d"), stock_data["open"][i], stock_data["high"][i], stock_data["low"][i], stock_data["close"][i], adjClose[i], stock_data["volume"][i]))

        if has_dividends:    
            dividends_output = os.path.join(os.path.dirname(__file__), "{}_dividends.csv".format(self.stock_abbr))
            with open(dividends_output, 'w') as d:
                d.write("Date,Amount\n")
                for key in dividends_dict:
                    d.write("{},{}\n".format(datetime.fromtimestamp(dividends_dict[key]["date"]).strftime("%Y-%m-%d"), dividends_dict[key]["amount"]))
        
    def run(self):
        info = self.getStockReqInfo()
        if info:
            response = self.getJsonData(info)
            if not response:
                self.response_code_signal.emit(6)
                return 
            else:
                try:
                    self.parseJsonData(response)
                    self.response_code_signal.emit(0)
                    LOGGER.info("Scrape successfully completed.")
                except:
                    LOGGER.error("%s", response)
                    self.response_code_signal(7)

                

    #Main purpose is from email function in main
    def logInfo(self, code, info):
        if code == 0:
            LOGGER.info(info)
        else:
           LOGGER.error(info)
        
        
