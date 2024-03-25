#This file is just to set up the logger for the main function

#Imports
import os, logging

LOGPATH = os.path.join(os.path.dirname(__file__), 'log_file.log')
LOG = logging.getLogger('Main Logger')
LOG.setLevel(logging.INFO)
output = logging.FileHandler(LOGPATH, 'w')
formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s - %(asctime)s', 'on %m/%d/%Y at %H:%M %p')
output.setFormatter(formatter)

LOG.addHandler(output)
