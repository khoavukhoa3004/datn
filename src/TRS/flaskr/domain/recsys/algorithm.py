from flaskr.domain.submission.submission_models import Submission
from flaskr.domain.recsys.recsys_models import Recommendation
from flaskr.domain.matrixfactorization.MF_models import MatrixFactorization, loadMatrix
from flaskr.domain.tcclassification.tcclassification_models import TcClassification
from flaskr.database import db
from constants.constants import list_testcase_ids
import random
import numpy as np
from constants.constants import NO_TC_1_RECOMMENDATION
from datetime import date, timedelta, time, datetime
from constants import hcm_time


def recommendation_1(submission_id, assignment_id, student_id):
  '''
  Random pick những testcase làm bị sai
  '''
  # lay Submission tuong ung voi submission_id
  # submission = db.session.execute(db.select(Submission).where(Submission.id==submission_id)).scalar_one()
  submission = Submission.query.filter_by(id=submission_id).first()

  tc_scores = np.array(submission.scores) ## type: list, mẫu ví dụ: [True, False, True,...]
  
  false_tc = (np.array(list_testcase_ids))[tc_scores == False]
  false_tc = [int(x) for x in false_tc]
  
  status = None

  if len(false_tc) < NO_TC_1_RECOMMENDATION:
    rec_tc = []
    status = 2
  else:
    rec_tc = random.sample(list(false_tc), NO_TC_1_RECOMMENDATION)
    status = 3

  # Cap nhat lai recommendation
  # recommendation = db.session.execute(db.select(Recommendation).where(Recommendation.submission_id==submission_id)).scalar_one()
  recommendation = Recommendation.query.filter_by(submission_id=submission_id).first()
  print(recommendation)
  # print('submission: ', )
  print('recommendation: ', recommendation)
  print('status: ', status)
  recommendation.status = status
  recommendation.list_testcase_id = rec_tc
  recommendation.save()

def recommendation_2(submission_id, assignment_id, student_id):
  '''
  Chọn những testcase có rating cao nhất từ matrix factorization
  '''
  # lay Submission tuong ung voi submission_id
  submission = Submission.query.filter_by(id = submission_id).first()
  
  tc_scores = np.array(submission.scores) ## type: list, mẫu ví dụ: [True, False, True,...]
  
  false_tc = (np.array(list_testcase_ids))[tc_scores == False] # list of ids
  false_tc = [int(x) for x in false_tc]

  # rec_tc = []
  # status = None
  if len(false_tc) < NO_TC_1_RECOMMENDATION:
    rec_tc = []
    status = 2
  else:
    # assignment_id = assignment_id.strip('"')
    last_MF = MatrixFactorization.query.filter_by(assignment_id=assignment_id, model_name='RSVD').order_by(MatrixFactorization.created_at.desc()).first()
    
    if not last_MF:
      recommendation_1(submission_id, assignment_id, student_id)
      return
    else:
      if student_id in last_MF.list_student_ids:
        # lay ra
        idx_student_id = last_MF.list_student_ids.index(student_id)
        mf_matrix = loadMatrix(last_MF.matrix_npz_path)
        list_tc_ratings = np.array(mf_matrix[idx_student_id])


      else:
        # tinh trung binh
        mf_matrix = loadMatrix(last_MF.matrix_npz_path)
        list_tc_ratings = np.mean(mf_matrix, axis=0)
        
      false_tc_ratings = list_tc_ratings[tc_scores == False]
      false_tc_rating_id = [(rating, tc_id) for rating, tc_id in zip(false_tc_ratings, false_tc)] # list of (rating, id)
      
      false_tc_rating_id = sorted(false_tc_rating_id, key=lambda x: x[0], reverse=True)
      
      # print(f'false_tc_rating_id: {false_tc_rating_id}') # for testing
      
      rec_tc = [x[1] for x in false_tc_rating_id]
      rec_tc = rec_tc[:NO_TC_1_RECOMMENDATION]
      status = 3
    
  # Cap nhat lai recommendation
  recommendation = Recommendation.query.filter_by(submission_id=submission_id).first()
  recommendation.status = status
  recommendation.list_testcase_id = rec_tc
  recommendation.save()
  
def recommendation_3(submission_id, assignment_id, student_id):
  '''
  Chọn những testcase có rating cao nhất từ matrix factorization
  '''
  # lay Submission tuong ung voi submission_id
  submission = Submission.query.filter_by(id = submission_id).first()
  
  tc_scores = np.array(submission.scores) ## type: list, mẫu ví dụ: [True, False, True,...]
  
  false_tc = (np.array(list_testcase_ids))[tc_scores == False] # list of ids
  false_tc = [int(x) for x in false_tc]
  
  # status = None

  # rec_tc = []

  if len(false_tc) < NO_TC_1_RECOMMENDATION:
    rec_tc = []
    status = 2
  else:
    last_MF = MatrixFactorization.query.filter_by(assignment_id=assignment_id, model_name='timeSVD').order_by(MatrixFactorization.created_at.desc()).first()
    print("last MF:", last_MF)
    if not last_MF:
      recommendation_1(submission_id, assignment_id, student_id)
      return
    else:
      if student_id in last_MF.list_student_ids:
        # lay ra
        idx_student_id = last_MF.list_student_ids.index(student_id)
        mf_matrix = loadMatrix(last_MF.matrix_npz_path)
        list_tc_ratings = np.array(mf_matrix[idx_student_id])
      else:
        # tinh trung binh
        mf_matrix = loadMatrix(last_MF.matrix_npz_path)
        list_tc_ratings = np.mean(mf_matrix, axis=0)
        
      false_tc_ratings = list_tc_ratings[tc_scores == False]
      false_tc_rating_id = [(rating, tc_id) for rating, tc_id in zip(false_tc_ratings, false_tc)] # list of (rating, id)
      
      false_tc_rating_id = sorted(false_tc_rating_id, key=lambda x: x[0], reverse=True)
      
      # print(f'false_tc_rating_id: {false_tc_rating_id}') # for testing
      
      rec_tc = [x[1] for x in false_tc_rating_id]
      rec_tc = rec_tc[:NO_TC_1_RECOMMENDATION]
      status = 3
    
  # Cap nhat lai recommendation
  recommendation = Recommendation.query.filter_by(submission_id=submission_id).first()
  recommendation.status = status
  recommendation.list_testcase_id = rec_tc
  recommendation.save()


def recommendation_4(submission_id, assignment_id, student_id):
  '''
  Chọn những testcase có rating cao nhất từ matrix factorization
  '''
  # lay Submission tuong ung voi submission_id
  submission = Submission.query.filter_by(id = submission_id).first()
  
  tc_scores = np.array(submission.scores) ## type: list, mẫu ví dụ: [True, False, True,...]
  
  false_tc = (np.array(list_testcase_ids))[tc_scores == False] # list of ids
  false_tc = [int(x) for x in false_tc]
  
  # status = None

  # rec_tc = []

  if len(false_tc) < NO_TC_1_RECOMMENDATION:
    rec_tc = []
    status = 2
  else:
    print('LSTM')
    # assignment_id = assignment_id.strip('"')
    last_MF = MatrixFactorization.query.filter_by(assignment_id=assignment_id, model_name='LSTM').order_by(MatrixFactorization.created_at.desc()).first()
    print("last MF:", last_MF)
    if not last_MF:
      recommendation_1(submission_id, assignment_id, student_id)
      return
    else:
      if student_id in last_MF.list_student_ids:
        # lay ra
        idx_student_id = last_MF.list_student_ids.index(student_id)
        mf_matrix = loadMatrix(last_MF.matrix_npz_path)
        list_tc_ratings = np.array(mf_matrix[idx_student_id])
      else:
        # tinh trung binh
        mf_matrix = loadMatrix(last_MF.matrix_npz_path)
        list_tc_ratings = np.mean(mf_matrix, axis=0)
      
      print('LSTM list tc rating: ', list_tc_ratings)
      false_tc_ratings = list_tc_ratings[0][tc_scores == False]
      false_tc_rating_id = [(rating, tc_id) for rating, tc_id in zip(false_tc_ratings, false_tc)] # list of (rating, id)
      
      false_tc_rating_id = sorted(false_tc_rating_id, key=lambda x: x[0], reverse=True)
      
      # print(f'false_tc_rating_id: {false_tc_rating_id}') # for testing
      
      rec_tc = [x[1] for x in false_tc_rating_id]
      rec_tc = rec_tc[:NO_TC_1_RECOMMENDATION]
      status = 3
    
  # Cap nhat lai recommendation
  recommendation = Recommendation.query.filter_by(submission_id=submission_id).first()
  recommendation.status = status
  recommendation.list_testcase_id = rec_tc
  recommendation.save()