import numpy as np
from functools import reduce
import time
from keras.models import Sequential
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional

from tensorflow.keras.optimizers import Adam

def root_mean_squared_error(y_true, y_pred):
    y_true = tf.cast(y_true, dtype=tf.float32)  # Cast y_true to float32
    y_pred = tf.convert_to_tensor(y_pred, dtype=tf.float32)
    return tf.sqrt(tf.reduce_mean(tf.square(y_pred - y_true), axis=-1))

class RSVD:
    def __init__(self, matrix, f=20):
        self.matrix = np.array(matrix)
        self.f = f
        self.bi = {}
        self.bu = {}
        self.qi = {}
        self.pu = {}
        self.avg = np.mean(self.matrix[:, 2])
        for i in range(self.matrix.shape[0]):
            user_id = self.matrix[i, 0]
            item_id = self.matrix[i, 1]
            self.bi.setdefault(item_id, 0)
            self.bu.setdefault(user_id, 0)
            self.qi.setdefault(item_id, np.random.random((self.f, 1)) / 10 * np.sqrt(self.f))
            self.pu.setdefault(user_id, np.random.random((self.f, 1)) / 10 * np.sqrt(self.f))

    def predict(self, user_id, item_id):
        self.bi.setdefault(item_id, 0)
        self.bu.setdefault(user_id, 0)
        self.qi.setdefault(item_id, np.zeros((self.f, 1)))
        self.pu.setdefault(user_id, np.zeros((self.f, 1)))
        rating = self.avg + self.bi[item_id] + self.bu[user_id] + np.sum(
            self.qi[item_id] * self.pu[user_id])

        if rating > 1:
            rating = 1
        if rating < 0:
            rating = 0
        return rating


    def train(self, steps=60, gamma=0.005, Lambda=0.02):
        for step in range(steps):

            rmse = 0.0
            
            for i in range(self.matrix.shape[0]):
                user_id = self.matrix[i, 0]
                item_id = self.matrix[i, 1]
                rating = self.matrix[i, 2]
                eui = rating - self.predict(user_id, item_id)
                rmse += eui ** 2
                self.bu[user_id] += gamma * (eui - Lambda * self.bu[user_id])
                self.bi[item_id] += gamma * (eui - Lambda * self.bi[item_id])
                tmp = self.qi[item_id]
                self.qi[item_id] += gamma * (eui * self.pu[user_id] - Lambda * self.qi[item_id])
                self.pu[user_id] += gamma * (eui * tmp - Lambda * self.pu[user_id])
            gamma = 0.9 * gamma
            rmse = np.sqrt(rmse / self.matrix.shape[0])

    def evaluate(self, test_data):
        test_data = np.array(test_data)
        num_samples = test_data.shape[0]
        rmse = 0.0

        for i in range(num_samples):
            user_id = test_data[i, 0]
            item_id = test_data[i, 1]
            rating = test_data[i, 2]

            predicted_rating = self.predict(user_id, item_id)
            e_ui = rating - predicted_rating
            rmse += e_ui ** 2

        rmse = np.sqrt(rmse / num_samples)

        return rmse
    
class timeSVD:
    def __init__(self, matrix, f=20):
        self.matrix = np.array(matrix)
        print(self.matrix)
        self.f = f
        self.b_i = {}
        self.b_u = {}
        self.b_t = {}
        self.q_i = {}
        self.p_u = {}
        self.x_u = {}
        self.z_t = {}
        self.s_i = {}
        self.y_w = {}
        self.g_u = {}
        self.l_i = {}
        self.h_t = {}
        self.avg = np.mean(self.matrix[:, 2])
        self.user_time = {}
        self.item_time = {}

        for i in range(self.matrix.shape[0]):
          if matrix[i][0] in self.user_time and matrix[i][3] < self.user_time[matrix[i][0]]:
            self.user_time[matrix[i][0]] = matrix[i][3]
          elif matrix[i][0] not in self.user_time:
            self.user_time[matrix[i][0]] = matrix[i][3]

          if matrix[i][1] in self.item_time and matrix[i][3] < self.item_time[matrix[i][1]]:
            self.item_time[matrix[i][1]] = matrix[i][3]
          elif matrix[i][1] not in self.item_time:
            self.item_time[matrix[i][1]] = matrix[i][3]

        for i in range(self.matrix.shape[0]):

            user_id = self.matrix[i, 0]
            item_id = self.matrix[i, 1]
            time = self.matrix[i, 3]
            t = time - self.user_time[user_id]
            w = time - self.item_time[item_id]

            self.b_i.setdefault(item_id, 0)
            self.b_u.setdefault(user_id, 0)
            self.b_t.setdefault(time, 0)

            self.q_i.setdefault(item_id, np.random.random((self.f, 1)) / 10 * np.sqrt(self.f))
            self.p_u.setdefault(user_id, np.random.random((self.f, 1)) / 10 * np.sqrt(self.f))

            self.x_u.setdefault(user_id, np.random.random((self.f, 1)) / 10 * np.sqrt(self.f))
            self.z_t.setdefault(t, np.random.random((self.f, 1)) / 10 * np.sqrt(self.f))

            self.s_i.setdefault(item_id, np.random.random((self.f, 1)) / 10 * np.sqrt(self.f))
            self.y_w.setdefault(w, np.random.random((self.f, 1)) / 10 * np.sqrt(self.f))

            self.g_u.setdefault(user_id, np.random.random((self.f, 1)) / 10 * np.sqrt(self.f))
            self.l_i.setdefault(item_id, np.random.random((self.f, 1)) / 10 * np.sqrt(self.f))
            self.h_t.setdefault(t, np.random.random((self.f, 1)) / 10 * np.sqrt(self.f))

    def preference(self, user_id, item_id, t):
      return reduce(lambda x, i: x+self.g_u[user_id][i][0]*self.l_i[item_id][i][0]*self.h_t[t][i][0], range(self.f),0)

    def predict(self, user_id, item_id, time):
      self.b_i.setdefault(item_id, 0)
      self.b_u.setdefault(user_id, 0)
      self.b_t.setdefault(time, 0)
      self.user_time.setdefault(user_id, time)
      self.item_time.setdefault(item_id, time)

      t = time - self.user_time[user_id]
      w = time - self.item_time[item_id]

      self.q_i.setdefault(item_id, np.zeros((self.f, 1)))
      self.p_u.setdefault(user_id, np.zeros((self.f, 1)))

      self.x_u.setdefault(user_id, np.zeros((self.f, 1)))
      self.z_t.setdefault(t, np.zeros((self.f, 1)))

      self.s_i.setdefault(item_id, np.zeros((self.f, 1)))
      self.y_w.setdefault(w, np.zeros((self.f, 1)))

      self.g_u.setdefault(user_id, np.zeros((self.f, 1)))
      self.l_i.setdefault(item_id, np.zeros((self.f, 1)))
      self.h_t.setdefault(t, np.zeros((self.f, 1)))

      rating =  self.avg + self.b_i[item_id] + self.b_u[user_id] + self.b_t[time] + \
                (self.p_u[user_id].T.dot(self.q_i[item_id]))[0][0] + \
                (self.x_u[user_id].T.dot(self.z_t[t]))[0][0] + \
                (self.s_i[item_id].T.dot(self.y_w[w]))[0][0] + \
                self.preference(user_id, item_id, t)

      if rating > 1:
        rating = 1
      if rating < 0:
        rating = 0
      return rating

    def train(self, steps=10, gamma=0.001, Lambda=0.05):

      for step in range(steps):

        print('step', step + 1, 'is running')
        rmse = 0.0

        start_time = time.time()
        for i in range(self.matrix.shape[0]):
          user_id = self.matrix[i][0]
          item_id = self.matrix[i][1]
          tim    = self.matrix[i][3]

          t = tim - self.user_time[user_id]
          w = tim - self.item_time[item_id]

          rating = self.matrix[i, 2]
          e_ui = rating - self.predict(user_id, item_id, tim)

          rmse += e_ui ** 2

          self.b_u[user_id] += gamma * (e_ui - Lambda * self.b_u[user_id])
          self.b_i[item_id] += gamma * (e_ui - Lambda * self.b_i[item_id])
          self.b_t[tim]    += gamma * (e_ui - Lambda * self.b_t[tim])

          pTemp = self.p_u[user_id]
          qTemp = self.q_i[item_id]
          xTemp = self.x_u[user_id]
          zTemp = self.z_t[t]
          sTemp = self.s_i[item_id]
          yTemp = self.y_w[w]
          gTemp = self.g_u[user_id]
          lTemp = self.l_i[item_id]
          hTemp = self.h_t[t]

          self.p_u[user_id] += gamma * (e_ui * qTemp - Lambda * pTemp)
          self.q_i[item_id] += gamma * (e_ui * pTemp - Lambda * qTemp)

          self.x_u[user_id] += gamma * (e_ui * zTemp - Lambda * xTemp)
          self.z_t[t]       += gamma * (e_ui * xTemp - Lambda * zTemp)

          self.s_i[item_id] += gamma * (e_ui * yTemp - Lambda * sTemp)
          self.y_w[w]       += gamma * (e_ui * sTemp - Lambda * yTemp)

          self.g_u[user_id] += gamma * (e_ui * lTemp * hTemp - Lambda * gTemp)
          self.l_i[item_id] += gamma * (e_ui * gTemp * hTemp - Lambda * lTemp)
          self.h_t[t]       += gamma * (e_ui * gTemp * lTemp - Lambda * hTemp)
        end_time = time.time()

        elapsed_time = end_time - start_time
        print(elapsed_time)
        gamma = 0.9 * gamma

        rmse = np.sqrt(rmse / self.matrix.shape[0])
        print(f'Epoch {step + 1}/{steps}: {rmse}')

    def evaluate(self, test_data):
        test_data = np.array(test_data)
        num_samples = test_data.shape[0]
        rmse = 0.0

        for i in range(num_samples):
            user_id = test_data[i, 0]
            item_id = test_data[i, 1]
            rating = test_data[i, 2]
            time = test_data[i, 3]

            predicted_rating = self.predict(user_id, item_id, time)
            e_ui = rating - predicted_rating
            rmse += e_ui ** 2

        rmse = np.sqrt(rmse / num_samples)

        return rmse
      
      
class LSTMModel:
  def __init__(self):
    self.history = None
    self.model = None
    
  def define_model(self, input_shape,learning_rate, hidden_unit=32 ,dropout=0.2, num_lstm_layer=1, direct_dropout=False, is_separated_dropout=False):
    model = Sequential()
    if direct_dropout:
      if num_lstm_layer == 1:
        model.add(LSTM(hidden_unit, input_shape=input_shape, dropout=dropout))
        if is_separated_dropout:
          model.add(LSTM(hidden_unit, dropout=dropout))
      elif num_lstm_layer == 2:
        model.add(LSTM(hidden_unit, return_sequences=True, input_shape=input_shape, dropout=dropout))
        if is_separated_dropout:
          model.add(Dropout(dropout))
        model.add(LSTM(hidden_unit, dropout=dropout))
        if is_separated_dropout:
          model.add(Dropout(dropout))
      elif num_lstm_layer == 3: 
        model.add(LSTM(hidden_unit, return_sequences=True, input_shape=input_shape, dropout=dropout))
        if is_separated_dropout:
          model.add(Dropout(dropout))
        model.add(LSTM(hidden_unit,return_sequences=True,dropout=dropout))
        if is_separated_dropout:
          model.add(Dropout(dropout))
        model.add(LSTM(hidden_unit))

      else:
        if num_lstm_layer == 1:
          model.add(LSTM(hidden_unit, input_shape=input_shape))
          model.add(Dropout(dropout))
        elif num_lstm_layer == 2:
          model.add(LSTM(hidden_unit, return_sequences=True, input_shape=input_shape))
          model.add(Dropout(dropout))
          model.add(LSTM(hidden_unit))
          model.add(Dropout(dropout))
        elif num_lstm_layer == 3: 
          model.add(LSTM(hidden_unit, return_sequences=True, input_shape=input_shape))
          model.add(Dropout(dropout))
          model.add(LSTM(hidden_unit, return_sequences=True))
          model.add(LSTM(hidden_unit))
          model.add(Dropout(dropout))
          
    model.add(Dense(input_shape[1], activation='sigmoid'))
    # model.add(Dense(input_shape[1]))
    
    # Compile the model with Adam optimizer and RMSE loss
    optimizer = Adam(learning_rate=learning_rate)
    
    model.compile(loss=root_mean_squared_error, optimizer=optimizer)
    # model.compile(loss=root_mean_squared_error, metrics=['mae'], optimizer=optimizer)
    self.model = model

  def define_new_model(self, input_shape):
    model = Sequential()
    model.add(Bidirectional(LSTM(256, return_sequences=True), input_shape=input_shape))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(128, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(64)))
    model.add(Dropout(0.3))
    model.add(Dense(input_shape[1], activation='softmax'))
    # Compile the model with Adam optimizer and RMSE loss
    optimizer = Adam(learning_rate=self.learning_rate)
    model.compile(loss='mean_squared_error', metrics=['mae'], optimizer=optimizer)
    return model
  
  def train(self, X_train, y_train, batch_size, epochs):
    self.history = self.model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, shuffle=False)
  
  def evaluate(self, X_test, y_test):

    evaluation = self.model.evaluate(X_test, y_test)
    return evaluation
  
  def predict(self, X_test):
    return self.model.predict(X_test)
  
  def summary(self):
      self.model.summary()
      
  def save(self, filename):
      self.model.save(filename)