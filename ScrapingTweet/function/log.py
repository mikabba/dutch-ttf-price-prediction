import logging

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
file_handler = logging.FileHandler('./log/log.log')
file_handler.setLevel(logging.DEBUG)

# create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def debug(text):
    logger.debug(text)
def info(text):
    logger.info(text)
def warning(text):
    logger.warning(text)
def error(text):
    logger.error(text)
def critical(text):
    logger.critical(text)

