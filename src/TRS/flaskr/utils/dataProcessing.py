class Dataset:
  def __init__(self):
    pass

  def load_dataset_timeSVD(self, dataset):

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
  
  def load_dataset_RSVD(self, dataset):

    df = []

    # Lặp qua từng hàng trong data
    for i, row in dataset.iterrows():
        score = int(row['rating'])
        student_id = int(row['student_id'])
        testcase_id = int(row['testcase_id'])

        df.append([student_id, testcase_id , score])

    # print(df)
    return df
  