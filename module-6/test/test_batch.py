import logging
import sys
from batch import *


if __name__=="__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info('starting the process')
    year = 2024 # hardcoding for testing
    month = 3 # hardcoding 
    logging.info(f"the input year -{year} and the output year is {month}")
    main(year,month)
