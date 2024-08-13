import numpy as np
from dotenv import dotenv_values
from pytz import timezone

env_config = dotenv_values('.env')

FILE_WITH_ID = env_config['FILE_WITH_ID']
FILE_SUBMISSION_PATH = env_config['FILE_SUBMISSION_PATH']
FILE_LIST_STUDENTS_PATH = env_config['FILE_LIST_STUDENTS_PATH']

DB_USER = env_config['DB_USER']
DB_PWD = env_config['DB_PWD']
DB_HOST = env_config['DB_HOST']
DB_NAME = env_config['DB_NAME']

DB_INIT = env_config['DB_INIT'] == 'True'

# Grader
GRADER_URL = env_config['GRADER_URL']

# Testcase config
NO_TC_1_RECOMMENDATION = int(env_config['NO_TC_1_RECOMMENDATION'])

# Group of student by initial scores
# and group with recommendation method
npz_group = np.load('files/input/A2_group_std.npz')
gteq8 = []
gteq5 = npz_group['gteq5']
gteq5 = [str(x) for x in gteq5]
lt5 = npz_group['lt5']

rec_apr1 = set([str(x) for x in npz_group['rec_apr1']])
rec_apr2 = set([str(x) for x in npz_group['rec_apr2']])
rec_apr3 = set([str(x) for x in npz_group['rec_apr3']])

list_testcase_ids = list(npz_group['list_testcase_ids']) # theo model, list_testcase_ids gồm các số nguyên, không phải string
list_testcase_ids = [int(x) for x in list_testcase_ids]
MAX_NO_THREADS = int(env_config['MAX_NO_THREADS'])

# Time zone
hcm_time = timezone('Asia/Ho_Chi_Minh')