from flaskr.submission.submission_models import Submission
from flaskr.recsys.recsys_models import Recommendation
from flaskr.matrixfactorization.MF_models import MatrixFactorization, loadMatrix
from flaskr.tcclassification.tcclassification_models import TcClassification
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
  submission = db.session.execute(db.select(Submission).where(Submission.id==submission_id)).scalar_one()
  
  tc_scores = np.array(submission.scores) ## type: list, mẫu ví dụ: [True, False, True,...]
  
  false_tc = (np.array(list_testcase_ids))[tc_scores == False]
  false_tc = [int(x) for x in false_tc]
  
  if len(false_tc) < NO_TC_1_RECOMMENDATION:
    rec_tc = []
    status = 2
  else:
    rec_tc = random.sample(list(false_tc), NO_TC_1_RECOMMENDATION)
    status = 3

  # Cap nhat lai recommendation
  recommendation = db.session.execute(db.select(Recommendation).where(Recommendation.submission_id==submission_id)).scalar_one()
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
  
  if len(false_tc) < NO_TC_1_RECOMMENDATION:
    rec_tc = []
    status = 2
  else:
    last_MF = MatrixFactorization.query.filter_by(assignment_id=assignment_id).order_by(MatrixFactorization.created_at.desc()).first()
    
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
  recommendation = db.session.execute(db.select(Recommendation).where(Recommendation.submission_id==submission_id)).scalar_one()
  recommendation.status = status
  recommendation.list_testcase_id = rec_tc
  recommendation.save()
  
def recommendation_3(submission_id, assignment_id, student_id):
  '''
  Chọn những testcase có rating cao nhất từ matrix factorization
  + chọn độ khó cao hơn / thấp hơn
  '''
  # lay Submission tuong ung voi submission_id
  submission = Submission.query.filter_by(id = submission_id).first()
  
  tc_scores = np.array(submission.scores) ## type: list, mẫu ví dụ: [True, False, True,...]
  
  false_tc = (np.array(list_testcase_ids))[tc_scores == False] # list of ids
  false_tc = [int(x) for x in false_tc]
  
  if len(false_tc) < NO_TC_1_RECOMMENDATION:
    rec_tc = []
    status = 2
    level = None
  else:
    # đọc testcase classification lên
    lastTcClass = TcClassification.query.filter_by(assignment_id = assignment_id).order_by(TcClassification.updated_at.desc()).first()
    
    list_testcase_levels = np.array(lastTcClass.list_testcase_levels)
    false_testcase_levels = list_testcase_levels[tc_scores == False]
    
    # đọc matrix factorization lên
    last_MF = MatrixFactorization.query.filter_by(assignment_id=assignment_id).order_by(MatrixFactorization.created_at.desc()).first()
    if student_id in last_MF.list_student_ids:
      # lay ra
      idx_student_id = last_MF.list_student_ids.index(student_id)
      mf_matrix = loadMatrix(last_MF.matrix_npz_path)
      list_tc_ratings = np.array(mf_matrix[idx_student_id])
    else:
      # tinh trung binh
      mf_matrix = loadMatrix(last_MF.matrix_npz_path)
      matrix = np.array(mf_matrix)
      # print(f'matrix = {matrix.shape}, path = {last_MF.matrix_npz_path}')
      list_tc_ratings = np.mean(matrix, axis=0)

    # print(f'list_tc_ratings = {list_tc_ratings.shape}, tc_scores = {tc_scores.shape}')
    false_tc_ratings = list_tc_ratings[tc_scores == False]
    false_tc_rating_id_level = [(rating, tc_id, level) for rating, tc_id, level in zip(false_tc_ratings, false_tc, false_testcase_levels)] # list of (rating, id, level)
    
    false_tc_rating_id_level = sorted(false_tc_rating_id_level, key=lambda x: x[0], reverse=True)
    
    # rec_tc = [x[1] for x in false_tc_rating_id_level]
    # rec_tc = rec_tc[:3] # 2 testcase còn lại lấy điều chỉnh theo độ khó
    rec_tc = []
    
    # Đếm số lần nộp hợp lệ trong ngày hôm trước
    # số lần hợp lệ: đều đã làm đúng hết các testcase
    # đếm bằng cách: đếm các recommendation thành công (status = 3)
    # trong ngày hôm trước
    today = date.today()
    pre_date = today + timedelta(days=-1)
    start = datetime.combine(pre_date, time=time(0,0,0))
    end = datetime.combine(today, time=time(0,0,0))
    # start = hcm_time.localize(start)
    # end = hcm_time.localize(end)
    
    # list_recommendation = db.session.execute(db.select(Recommendation).where(Recommendation.submission_id==submission_id).where(Recommendation.status == 3).where(Recommendation.updated_at >= start).where(Recommendation.updated_at <= end).order_by(Recommendation.updated_at.desc())).all()
    
    list_recommendation = Recommendation.query.join(Submission, Recommendation.submission_id == Submission.id).filter(Submission.student_id == student_id).filter(Recommendation.status == 3).filter(Recommendation.updated_at >= start).filter(Recommendation.updated_at <= end).order_by(Recommendation.updated_at.desc()).all()
    # giảm dần theo thời gian
    
    # last_r_t = Recommendation.query.filter(Recommendation.status == 3).order_by(Recommendation.updated_at.desc()).first()
    # print(f'len(list_recommendation) = {len(list_recommendation)}')
    # print(f'start = {start}, end = {end}, lastr = {last_r_t.updated_at}, lastr >= start: {last_r_t.updated_at >= start}, lastr <= end: {last_r_t.updated_at <= end}')
    print(f'algorithm 3 - len(list_recommendation) = {len(list_recommendation)}, student_id = {student_id}', flush=True)
    if len(list_recommendation) == 0:
      level = 1 # de
    elif len(list_recommendation) <= 2:
      # nộp 1 / 2 lần, quá khó -> điều chỉnh dễ hơn
      level = list_recommendation[0].level - 1
    elif len(list_recommendation) == 3:
      # nộp 3 lần, bình thường, độ khó giữa nguyên
      level = list_recommendation[0].level
    else:
      # nộp 4, 5 lần, dễ -> điều chỉnh khó hơn
      level = list_recommendation[0].level + 1
    
    # level phải nằm trong khoảng [1, 2, 3]
    if level < 1: level = 1
    if level > 3: level = 3
    
    level_temp = level
    
    while level_temp <= 3:
      l = []
      for rating, id, lv in false_tc_rating_id_level:
        if lv == level_temp:
          l.append((rating, id))
          
      l = sorted(l, key=lambda x: x[0], reverse=True) # (rating, id)
      # lt = [x[1] for x in l]
      
      for r, tcid in l:
        if not tcid in rec_tc:
          rec_tc.append(tcid)
          
      # rec_tc = rec_tc + lt
      
      if len(rec_tc) >= NO_TC_1_RECOMMENDATION:
        rec_tc = rec_tc[:NO_TC_1_RECOMMENDATION]
        break
      
      level_temp += 1
    
    if len(rec_tc) < NO_TC_1_RECOMMENDATION:
      rec_tc = []
      status = 2 # không đủ testcase để gợi ý
    else:
      status = 3
    
  # Cap nhat lai recommendation
  recommendation = db.session.execute(db.select(Recommendation).where(Recommendation.submission_id==submission_id)).scalar_one()
  recommendation.status = status
  recommendation.list_testcase_id = rec_tc
  if level is not None:
    recommendation.level = level
  recommendation.save()