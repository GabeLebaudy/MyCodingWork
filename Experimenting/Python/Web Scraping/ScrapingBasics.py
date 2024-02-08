#This file will be used to demonstrate the basics of python web scraping

#Imports
from bs4 import BeautifulSoup as bs
import requests
import os

#Read data from a downloaded HTML file
def readHtmlFile():
    file_path = os.path.join(os.path.dirname(__file__), 'HTMLBasicsDemo.html')

    with open(file_path, 'r') as f:
        #Unload file content into a Beautiful soup object
        file_content = f.read()
        soup_obj = bs(file_content, 'lxml')

    #Prints out HTML code in a readable format
    #print(soup_obj.prettify())

    #Find a specific tag
    h1_tag = soup_obj.find('h1')
    print(h1_tag)

    #Find all instances of a type of element
    link_elements = soup_obj.find_all('a')
    #print(link_elements)

    #Extract the text from an element
    print(link_elements[1].text)

    #Extract Elements with a certain class
    list_elements = soup_obj.find_all('li', class_ = 'First Class')
    for element in list_elements:
        print(element.text)


#Read from a webpage
def readWebPage():
    html_text = requests.get('https://www.youtube.com/@thatsgoodsports').text
    
    yt = bs(html_text, 'lxml')

    element_to_search = None
    for element in yt:
        if element.text == "ThatsGoodSports":
            element_to_search = element
        else:
            print(element.text)
    
    print(element_to_search)
    

#Main Method
if __name__ == "__main__":
    #Example method reading from a HTML file
    readHtmlFile()
    readWebPage()
