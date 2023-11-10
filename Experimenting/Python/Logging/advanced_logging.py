#This file will be used for the advanced logging tutorial from python's HOW TO for logging

#imports
import logging
import os

LOGPATH = os.path.join(os.path.dirname(__file__), 'advanced_logging.log')

#Main method
if __name__ == "__main__":
    #Creating a logger object instead of directly using the logging library
    logger = logging.getLogger('Advanced Logging')
    logger.setLevel(logging.INFO)

    output = logging.FileHandler(LOGPATH, 'w')
    formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s - %(asctime)s', 'on %m/%d/%Y at %H:%M %p')
    output.setFormatter(formatter)

    logger.addHandler(output)

    logger.debug("This shouldn't be added")
    logger.info('This should be added')
    logger.warning('Yo! Watch out!')
    