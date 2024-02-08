#This file will be used for dads webpage

#Imports
from bs4 import BeautifulSoup as soup
import requests
import os


#Get HTML Code
def getHTML():
    html = requests.get('https://www.google.com/get/videoqualityreport/').text
    data = soup(html, 'lxml')
    
    elements = data.find_all('div')
    chart_div = None
    for e in elements:
        if 'class' in e.attrs:
            if e['class'] == ['chart']:
                chart_div = e
                break
    
    


    
#Main Method
if __name__ == "__main__":
    getHTML()