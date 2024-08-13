import os
from datetime import date  

PATH_SEP = os.path.sep

bind = '0.0.0.0:5002'
workers = 1
loglevel = 'debug'
errorlog = f"logs{PATH_SEP}{date.today().strftime('%d-%m-%Y')}.log"
print_config = False
capture_output = True