#This file will be used to test out most of the basic features of the default python logging library

#Imports
import logging
import os
import time

#Sample Method
def addTwoNumbers(a, b):
    logging.info('Function Called')
    return a + b

#Main Method
if __name__ == "__main__":
    #Simple Example:
    """ logging.warning('Yo! Duck!') #This will print to the console, as the default behavior is to print out all logging info that exceeds the warning level
    logging.error('Watch out fool!') #This will print too
    logging.info('All good over here!') #This won't print, it's below the warning level """

    #Routing the messages to a logging file
    logPath = os.path.join(os.path.dirname(__file__), 'logging.log')
    #logging.basicConfig(filename=logPath, encoding='utf-8', level=logging.DEBUG, filemode='w')

    """ logging.debug('This message will be written to the log file')
    logging.info('This should also be written. Standard info message.')
    logging.warning('Like in the console, this message will be written to the file.')
    logging.error('This is an error message.') """

    #Example of logging the process of running a function
    """ logging.info('Function Started')
    print(addTwoNumbers(10, 12))
    logging.info('Function Finished') """

    #Example of logging variable data formatted into strings
    """ fruit = 'apples'
    vegetable = 'corn'
    amount = 10

    logging.warning('There are only %d %s and also %d %s', amount, fruit, amount, vegetable) """

    #Chaning the format of displayed messages
    """ logging.basicConfig(filename=logPath, encoding='utf-8', level=logging.DEBUG, filemode='w', format='%(levelname)s: %(message)s') #Level name controls the level (i.e. info, warning, error) and message shows the passed in string
    logging.debug('This is what a debug statement looks like.')
    logging.info('Heres an info statement')
    logging.warning('And a warning for you dawg.') """

    #Displaying date and time of messages
    logging.basicConfig(filename=logPath, encoding='utf-8', level=logging.DEBUG, filemode='w', datefmt='%m/%d/%Y %I:%M:%S %p', format='%(levelname)s: %(message)s at %(asctime)s') #Date format is the same as the time.strftime() formatting
    logging.info('This is the first log message!')
    time.sleep(2)
    logging.info('This is the second message!')






