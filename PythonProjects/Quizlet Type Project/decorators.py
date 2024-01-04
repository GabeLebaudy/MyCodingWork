#This file will be used for decorator functions.

#Imports
import logging
import os

from PyQt6.QtGui import QGuiApplication

#Logging
LOGPATH = os.path.join(os.path.dirname(__file__), 'log_file.log')
LOGGER = logging.getLogger('Main Logger')
LOGGER.setLevel(logging.INFO)
output = logging.FileHandler(LOGPATH, 'w')
formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s - %(asctime)s', 'on %m/%d/%Y at %H:%M %p')
output.setFormatter(formatter)

LOGGER.addHandler(output)

#Log the start and stop of a function
def log_start_and_stop(f):
    def wrapper(*args, **kwargs):
        LOGGER.info('Starting ' + f.__name__ + '...')
        result = f(*args, **kwargs)
        LOGGER.info('Finished ' + f.__name__ + '.')
        return result
    return wrapper

