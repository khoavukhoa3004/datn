import numpy as np
from functools import reduce

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
            self.qi.setdefault(item_id, np.random.generator((self.f, 1)) / 10 * np.sqrt(self.f))
            self.pu.setdefault(user_id, np.random.generator((self.f, 1)) / 10 * np.sqrt(self.f))

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


    def train(self, steps=60, gamma=0.005, _lambda=0.02):
        for step in range(steps):

            rmse = 0.0
            KK = np.random.Generator(self.matrix.shape[0])
            
            for i in range(self.matrix.shape[0]):
                j = KK[i]
                user_id = self.matrix[j, 0]
                item_id = self.matrix[j, 1]
                rating = self.matrix[j, 2]
                eui = rating - self.predict(user_id, item_id)
                rmse += eui ** 2
                self.bu[user_id] += gamma * (eui - _lambda * self.bu[user_id])
                self.bi[item_id] += gamma * (eui - _lambda * self.bi[item_id])
                tmp = self.qi[item_id]
                self.qi[item_id] += gamma * (eui * self.pu[user_id] - _lambda * self.qi[item_id])
                self.pu[user_id] += gamma * (eui * tmp - _lambda * self.pu[user_id])
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
    
class TimeSVD:
    def __init__(self, matrix, f=20):
        self.matrix = np.array(matrix)
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
      return reduce(lambda x, i: x+self.g_u[user_id][i]*self.l_i[item_id][i]*self.h_t[t][i], range(self.f),0)

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
                self.p_u[user_id].T.dot(self.q_i[item_id]) + \
                self.x_u[user_id].T.dot(self.z_t[t]) + \
                self.s_i[item_id].T.dot(self.y_w[w]) + \
                self.preference(user_id, item_id, t)

      if rating > 1:
        rating = 1
      if rating < 0:
        rating = 0
      return rating

    def train(self, steps=10, gamma=0.02, _lambda=0.035):
      for step in range(steps):
        rmse = 0.0
        for i in range(self.matrix.shape[0]):
          user_id = self.matrix[i][0]
          item_id = self.matrix[i][1]
          time    = self.matrix[i][3]

          t = time - self.user_time[user_id]
          w = time - self.item_time[item_id]

          rating = self.matrix[i, 2]
          e_ui = rating - self.predict(user_id, item_id, time)

          rmse += e_ui ** 2

          self.b_u[user_id] += gamma * (e_ui - _lambda * self.b_u[user_id])
          self.b_i[item_id] += gamma * (e_ui - _lambda * self.b_i[item_id])
          self.b_t[time]    += gamma * (e_ui - _lambda * self.b_t[time])

          for k in range(self.f):
            pTemp = self.p_u[user_id][k][0]
            qTemp = self.q_i[item_id][k][0]
            xTemp = self.x_u[user_id][k][0]
            zTemp = self.z_t[t][k][0]
            sTemp = self.s_i[item_id][k][0]
            yTemp = self.y_w[w][k][0]
            gTemp = self.g_u[user_id][k][0]
            lTemp = self.l_i[item_id][k][0]
            hTemp = self.h_t[t][k][0]

            self.p_u[user_id][k][0] += gamma * (e_ui * qTemp - _lambda * pTemp)
            self.q_i[item_id][k][0] += gamma * (e_ui * pTemp - _lambda * qTemp)

            self.x_u[user_id][k][0] += gamma * (e_ui * zTemp - _lambda * xTemp)
            self.z_t[t][k][0]       += gamma * (e_ui * xTemp - _lambda * zTemp)

            self.s_i[item_id][k][0] += gamma * (e_ui * yTemp - _lambda * sTemp)
            self.y_w[w][k][0]       += gamma * (e_ui * sTemp - _lambda * yTemp)

            self.g_u[user_id][k][0] += gamma * (e_ui * lTemp * hTemp - _lambda * gTemp)
            self.l_i[item_id][k][0] += gamma * (e_ui * gTemp * hTemp - _lambda * lTemp)
            self.h_t[t][k][0]       += gamma * (e_ui * gTemp * lTemp - _lambda * hTemp)

        gamma = 0.9 * gamma
        rmse = np.sqrt(rmse / self.matrix.shape[0])[0][0]

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