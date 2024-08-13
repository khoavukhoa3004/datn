import pandas as pd
import numpy as np
import random
from functools import reduce
from datetime import datetime

class Dataset:
  def __init__(self):
    self.user_time = None
    self.item_time = None

  def onlyDate(self, time):
    date_part = time.split(" ")[0]
    date_object = datetime.strptime(date_part, "%Y-%m-%d").date()
    return date_object

  def convertTime(self, time_str):
    time_parts = time_str.split("+")
    time_without_timezone = time_parts[0]
    
    original_time = datetime.strptime(time_without_timezone, "%Y-%m-%d %H:%M:%S.%f")

    # Đặt phút và giây về 0
    original_time = original_time.replace(minute=0, second=0, microsecond=0)

    # In kết quả
    return original_time

  def load_dataset(self, path, train_size=0.85):
    data = pd.read_csv(path)
    data = data[['student_id', 'id',  'scores', 'created_at']]
    #lưu lại ngày tháng sử dụng testcase
    data['created_at'] = data['created_at'].astype(str)
    data['created_at'] = data['created_at'].apply(lambda x: self.convertTime(x))

    data['scores'] = data['scores'].apply(lambda x: x.replace('{','').replace('}','').replace(',',''))
    df = []
    # Lặp qua từng hàng trong data
    for i, row in data.iterrows():
        scores = row['scores']
        student_id = row['student_id']

        # Lặp qua từng ký tự trong scores
        for j, score in enumerate(scores):
            value = 1 if score == 't' else 0
            df.append([student_id, j, value, row['created_at']])

    #Lưu lại thời điểm lần đầu tiên sinh viên sử dụng hệ thống
    data['created_at'] = pd.to_datetime(data['created_at'])

    #Lưu lại thời điểm lần đầu tiên sinh viên sử dụng hệ thống
    self.user_time = data.groupby('student_id')['created_at'].min()

    #Lưu lại thời điểm lần đầu tiên item được sử dụng
    self.item_time = data.groupby('id')['created_at'].min()
    np.random.seed(1234)
    random.shuffle(df)

    # Tính chỉ số để chia dữ liệu thành tập train, validation, và test
    num_samples = len(df)
    train_size = int(num_samples * train_size)

    train_data = df[:train_size]
    test_data = df[train_size:]

    return train_data, test_data, df