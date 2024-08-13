import pandas as pd
import numpy as np
import random
from functools import reduce
from datetime import datetime

class Dataset:
  def __init__(self):
    pass

  def load_dataset(self, dataset):

    df = []
    min_time = dataset['created_at'].min()

    # Lặp qua từng hàng trong data
    for i, row in dataset.iterrows():
        score = int(row['rating'])
        student_id = int(row['student_id'])
        testcase_id = int(row['testcase_id'])
        created_at = int(row['created_at'])

        df.append([student_id, testcase_id , score, (created_at-min_time)/3600])

    # print(df)
    return df
  
  