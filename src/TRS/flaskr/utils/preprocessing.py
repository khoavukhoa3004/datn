import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy 

class LSTMDataSet:
    def __init__(self, dataset: pd.DataFrame, timesteps = 1):
        '''
        dataset includes 3 columns:
            - student_id: str
            - updated_at: timestamp
            - scores: list[1,0....] 
        '''
        self.history = dict() # dict contains 
        self.dataset = dataset
        self.timesteps = timesteps
        self.mapped_student_ids = None
        # store number of true/false in scores. Student_id may be included
        self.score_count = -1
        self.x_shape = None
        self.dataset = self.prepare_dataset(self.dataset)
        
    def prepare_dataset(self,dataset: pd.DataFrame)-> pd.DataFrame:
        dataset.updated_at = pd.to_datetime(dataset['updated_at']).apply(lambda x: x.timestamp()).astype(float)

        # dataset = dataset[dataset['scores'].apply(lambda x: x != '{}')]
        # dataset.loc[:, 'scores'] = dataset['scores'].apply(lambda x: [1 if item.strip() == 't' else 0 for item in x.replace('\{', '').replace('\}', '').split(',')])
        self.score_count = len(dataset['scores'][0])
        
        dataset = dataset[['updated_at', 'student_id', 'scores']]
        dataset.loc[:, 'updated_at'] = pd.to_datetime(dataset['updated_at'], unit='s')
        dataset.sort_values('updated_at', inplace=True)
        return dataset
    
    def split_train_test_data_by_date(self, date_train_size: int, date_test_size: int):
        '''
        The data for testing is chosen by getting the last submissions based on number of days.
        Input: ratio: - array list(train,test): the ratio of train:test per user 
                      - int: the number of the last submissions for testing per user.
        For example: train_ratio=2, test_ratio=1, time_step=3
            user1: [submission1, submission2, submission3,...submission5]
            => [
                [submission1, submission2, submission3]
                [submission2, submission3, submission4]
                [submission3, submission4, submission5]
            ]
            -> train: [
                [submission1, submission2, submission3]
                [submission2, submission3, submission4]
            ]
            -> test is: [[submission3, submission4, submission5]]
        The shape of the data will be saved and you can get by calling method shape()
        Return: X_train, X_test, y_train, y_test
        '''
        end_date_train = self.dataset['updated_at'].min().normalize() + pd.DateOffset(date_train_size)
        end_date_test = end_date_train + pd.DateOffset(date_test_size)

        train_data = self.dataset[self.dataset['updated_at'] < end_date_train]
        test_data = self.dataset[(self.dataset['updated_at'] >= end_date_train) & (self.dataset['updated_at'] < end_date_test)]
        
        latest_records = train_data.groupby('student_id').apply(lambda x: x.nlargest(self.timesteps, 'updated_at')).reset_index(drop=True)
        latest_records = latest_records[latest_records['student_id'].isin(test_data['student_id'])]
        
        test_data = pd.concat([test_data, latest_records], ignore_index=True)
        test_data.sort_values('updated_at', inplace=True)
        X_train = []
        X_test = []
        y_train = []
        y_test = []
        for student_id, group in train_data.groupby('student_id'):
            submissions = group['scores'].values.tolist()
            temp_train_x, temp_train_y = self.slide_window(len(submissions), submissions)
            X_train = X_train + temp_train_x
            y_train = y_train + temp_train_y
        
        for student_id, group in test_data.groupby('student_id'):
            submissions = group['scores'].values.tolist()
            
            temp_train_x, temp_train_y = self.slide_window(len(submissions), submissions)
            X_test = X_test + temp_train_x
            y_test = y_test + temp_train_y
        X_train = np.array(X_train)
        X_test = np.array(X_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)
        self.x_shape = [X_train.shape[1], X_train.shape[2]]
        return X_train, X_test, y_train, y_test
    
    def train_all(self): 
        '''
        Similar to split_train_test_data_by_date but we will take all sumissions for training.
        '''
        train_data = self.dataset
        train_data.sort_values('updated_at', inplace=True)
        X_train = []
        y_train = []
        
        for student_id, group in train_data.groupby('student_id'):
            submissions = group['scores'].values.tolist()
            self.history[student_id] = submissions
            temp_train_x, temp_train_y = self.slide_window(len(submissions), submissions)
            X_train = X_train + temp_train_x
            y_train = y_train + temp_train_y
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        self.x_shape = [X_train.shape[1], X_train.shape[2]]
        return X_train, y_train
    
    def padding(self, num_submissions, submissions):
        if num_submissions < self.timesteps + 1:
            padding = [0] * self.score_count
            new_submission = copy.copy(submissions)
            new_submission = padding * (self.timesteps + 1 - num_submissions) + new_submission
            return new_submission
        return submissions
               
    def slide_window(self, num_submissions: int, submissions):  
        '''
        Input:  @param: num_submissions: number of submissions
                @param: submissions: list of all submissions ([[1,0,0,1], [1,1,1,0]...])
        Output: 2 array having shape (samples, timestep, features) and (output_feature)
        '''
        if self.score_count < 1:
            raise Exception("Score count must be greater than zero!")
        input_sequences = []
        target_values = [] 
        
        submissions = self.padding(num_submissions, submissions)
            
        if num_submissions >= self.timesteps + 1:
            for i in range(num_submissions - self.timesteps):
                window = submissions[i: i+self.timesteps]
                target = submissions[i+self.timesteps]
                
                # Pad or truncate each window to have a length of 5
                window = window[:self.timesteps] + [0] * max(0, self.timesteps - len(window))
                
                # Convert each element in the window to have a shape of (124,)
                window = [np.array(submission + [0] * max(0, self.score_count - len(submission))) for submission in window]
                
                # Prepare the target value with shape (124,)
                target = np.array(target + [0] * max(0, self.score_count - len(target)))
                
                input_sequences.append(window)
                target_values.append(target)
        return input_sequences, target_values

    def shape(self):
        return self.x_shape[0], self.x_shape[1]

    def describe_dataset(self, title):
        num_submissions = []
        for _, group in self.dataset.groupby('student_id'):
            submissions = group['scores'].values.tolist()
            num_submissions.append(len(submissions))
        plt.plot(num_submissions, label='Number of submissions')
        plt.ylabel('Num. of submissions')
        plt.title(title)
        plt.legend()
        plt.show()
        
        correct_counts = [0 for item in range(self.score_count)]
        prev = -1
        for index, row in self.dataset.iterrows():
            # Access the values of each column for the current row
            scores = row['scores']
            # print(scores)
            # print("hello")
            if prev == -1:
                prev= len(row['scores'])
            else:
                if prev != len(row['scores']):
                    print("-----")
                    print(row)
                    print(prev, len(row['scores']))
                    print(index)
                    print(row['scores'])
                    print("-----")  
                prev= len(row['scores'])
            for i in range(self.score_count):
                # print(i)
                correct_counts[i] = (correct_counts[i]+1) if (scores[i] == 1) else correct_counts[i]
        
        testcase_labels = [f'{i+1}' for i in range(len(correct_counts))]
        # Plotting the chart
        # plt.bar(testcase_labels, correct_counts)
        # plt.xlabel('Testcase')
        # plt.ylabel('Number of Correct Test Cases')
        # plt.title('Number of Correct Test Cases per Testcase '+ title)
        # plt.xticks(rotation=45)
        # plt.show()
