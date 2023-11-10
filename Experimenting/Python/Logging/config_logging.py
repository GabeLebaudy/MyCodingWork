#This file will be used to demonstrate importing a logger from a config file

#Imports
import logging
import logging.config
import os

#Paths for logging
LOGPATH = os.path.join(os.path.dirname(__file__), 'config_logging.log')
CONFIGPATH = os.path.join(os.path.dirname(__file__), 'config_logging.conf')

#Main method
if __name__ == "__main__":
    logging.config.fileConfig(CONFIGPATH)

    logger = logging.getLogger('fileConfigLogger')

    logger.debug('This wont print')
    logger.info('This will!')
    logger.warning('GTFO!')