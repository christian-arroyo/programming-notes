import os
import logging

# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

log_file = 'app.log'
FORMAT = '%(asctime)s %(message)s'

# if os.path.exists(log_file):
#     print('{0} exists'.format(log_file))
# else:
#     print("{0} does not exist".format(log_file))


logging.basicConfig(filename=log_file, filemode='a', level='DEBUG', format=FORMAT)
logging.warning('This will get logged')

logging.info('This is an info message')
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
