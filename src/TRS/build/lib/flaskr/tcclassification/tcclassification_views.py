from flaskr.submission.submission_models import Submission
from flaskr.database import db
from sqlalchemy import select
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
from flaskr.tcclassification.tcclassification_models import TcClassification

def buildClassification(app):
  with app.app_context():
    assignment_id = '49107748-1f4e-4dcf-8da2-12b5c3721e67'
    
    # load all last submission of each student
    stmt = select(Submission.student_id, Submission.assignment_id, Submission.scores, db.func.max(Submission.created_at)).where(Submission.assignment_id == assignment_id).group_by(Submission.student_id, Submission.assignment_id, Submission.scores)
    result = db.session.execute(stmt)
    
    list_subs = result.all()
    
    from constants import list_testcase_ids as list_tcs
    # list_tcs = [str(x) for x in range(1001, 1125)] # hard-code
    
    list_true_tcs = [0 for _ in list_tcs] # count number of student have right answer in a testcases
    
    for sub in list_subs:
      scores = sub[2]
      for idx, sc in enumerate(scores):
        if sc == True:
          list_true_tcs[idx] += 1
          
    # normalization
    list_true_tcs = np.array([x / len(list_subs) for x in list_true_tcs])
    
    # classification with kmean
    km = KMeans(n_clusters=3)
    data = np.array([[x] for x in list_true_tcs])
    labels = km.fit_predict(data)
    
    sil_score = silhouette_score(data, labels)
    
    unique_labels = np.unique(labels)
    list_label_avg = [] # (label, avg_score)

    for l in unique_labels:
      avg = np.mean(list_true_tcs[labels == l])
      list_label_avg.append((l, avg))
      
    list_label_avg = sorted(list_label_avg, key=lambda x: x[1], reverse=True) # list giảm dần theo avg_score
    # phần tử đầu tiên có điểm cao nhất -> dễ nhất
    
    dic = {} # map từ label sang độ khó
    for idx, (l, avg) in enumerate(list_label_avg):
      level = idx + 1 #  vị trí đầu tiên là dễ nhất
      dic[l] = level
      
    list_testcase_levels = [dic[l] for l in labels]
    
    tccls = TcClassification(list_testcase_ids=list_tcs, list_testcase_levels=list_testcase_levels,assignment_id=assignment_id,silhouette_score=sil_score)
    tccls.save()
    print('buildClassification done')