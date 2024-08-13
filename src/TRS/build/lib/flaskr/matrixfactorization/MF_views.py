from flaskr.submission.submission_models import Submission
from sqlalchemy import select
from flaskr.database import db
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import GridSearchCV
from flaskr.matrixfactorization.MF_models import MatrixFactorization, saveMatrix, loadMatrix
from flaskr.utils.time import timeNow
import numpy as np
from sqlalchemy.sql import text

def buildMF(app):
  with app.app_context():
    assignment_id = '656f8db9-851e-41db-8fab-11c8c7e2ae23'
    print('start buildMF')
    # load all last submission of each student
    # stmt = select(Submission.student_id, Submission.assignment_id, Submission.scores, db.func.max(Submission.created_at)).where(Submission.assignment_id == assignment_id).group_by(Submission.student_id, Submission.assignment_id, Submission.scores)
    # result = db.session.execute(stmt)
    
    # list_subs = result.all()
    query = '''
    select s2.student_id, max(s2.updated_at) as updated_at, max(scores) as scores 
    from ( 
      select siner.student_id, max(siner.updated_at) as max_updated_at 
      from submissions siner 
      group by student_id 
    ) s1 
    right outer join submissions s2 
    on (s1.student_id = s2.student_id 
      and s1.max_updated_at = s2.updated_at) 
    group by s2.student_id
    '''
    result = db.session.execute(text(query))
    # result = db.session.execute(stmt)
    list_subs = result.all() # list of (student_id, updated_at, scores)
    
    # list_tcs = [str(x) for x in range(1001, 1125)] # hard-code
    from constants import list_testcase_ids as list_tcs
    
    list_student_ids = []
    list_testcase_ids = []
    list_ratings = []
    # convert to dataframe
    # print(f'len = {len(list_subs)}, {list_subs[0]}')
    # assert(False)
    for sub in list_subs:
      student_id = sub[0]
      scores = sub[2]
      
      for idx, sc in enumerate(scores):
        list_student_ids.append(student_id)
        list_testcase_ids.append(list_tcs[idx])
        list_ratings.append(1 if sc else 0)
    
    df = pd.DataFrame()
    df['student_id'] = list_student_ids
    df['testcase_id'] = list_testcase_ids
    df['rating'] = list_ratings
    
    
    # SVD
    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(df, reader)
    
    param_grid = {"n_epochs": [5, 100], "n_factors": [5, 50]} # old: 10 -> 100
    gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=3)

    gs.fit(data)
    
    print('best score:', gs.best_score["rmse"])
    print('best param:', gs.best_params["rmse"])
    # print(len(df))
    
    # print(df.head())
    
    algo = gs.best_estimator["rmse"]
    algo.fit(data.build_full_trainset())
    
    # p = algo.predict('2211583', '1001', 1)
    # print(p)
    # print(p.est)
    
    # insert into database: MF
    db_list_tc_ids = list_tcs
    db_list_students_id = []
    db_matrix = []
    for sub in list_subs:
      student_id = sub[0]
      scores = sub[2]
      
      db_list_students_id.append(student_id)
      scores = [1 if x else 0 for x in scores]
      scores_predict = [None for x in scores]
      
      for idx, sc in enumerate(scores):
        scores_predict[idx] = algo.predict(student_id, db_list_tc_ids[idx], sc).est
        
      db_matrix.append(scores_predict)
    
    time_now = timeNow()
    npz_name = f'{time_now}_mf.npz'
    npz_path = f'files/matries/{npz_name}'
    db_matrix = np.array(db_matrix)
    saveMatrix(db_matrix, npz_path)
    mf = MatrixFactorization(list_student_ids=db_list_students_id, list_testcase_ids=db_list_tc_ids, assignment_id=assignment_id, matrix_npz_path=npz_path)
    mf.save()
    print('buildMF done')
  
  
def exportInitMF(app):
  with app.app_context():
    mf = MatrixFactorization.query.first()
    print(mf.id)
    m = mf.matrix
    saveMatrix(m, 'files/matries/m.npz')