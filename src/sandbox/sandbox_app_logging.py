import sys
import logging


log_formatter = logging.Formatter(
    fmt="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# file handler
file_handler = logging.FileHandler("example.log")
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)

# console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)


logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
