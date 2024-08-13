import logging
from flask import Blueprint, request, Response
from flask.globals import current_app
from flask.json import jsonify
from flaskr.utils.file import File
from constants import FILE_SUBMISSION_PATH, GRADER_URL
from werkzeug.utils import secure_filename
import os
from flaskr.utils.time import timeNow
from sqlalchemy import select
from flaskr.database import db
from flaskr.student.student_models import Student
from flaskr.submission.submission_models import Submission
from flaskr.assignment.assignment_models import Assignment
from flaskr.recsys.recsys_models import Recommendation
from flaskr.recsys.recsys_models import Recommendation
import requests
import threading
from flask import copy_current_request_context
from response import success, fail
from constants.constants import rec_apr1, rec_apr2, rec_apr3
from flaskr.recsys.algorithm import recommendation_4, recommendation_2, recommendation_3
from datetime import date, timedelta, time, datetime
from constants.constants import list_testcase_ids as Clist_testcase_ids
from flaskr.utils.text import encrypt, decrypt
from flask import render_template
from flaskr.utils.file import readall
from flaskr.utils.limitthread import LimitThread

blueprint = Blueprint('recsys', __name__)

@blueprint.route('/api/hello', methods=['GET',])
def hello():
  return 'Hello'

@blueprint.route('/api/recommend', methods=['POST',])
def receive_file():
  student_id = request.form.get('student_id')
  print(f'student_id = {student_id}', flush=True)
  assignment_name = request.form.get('assignment_name')
  
  if not File.checkStudentId(student_id):
    return {
      'status': 'fail',
      'data': [],
      'message': f'Invalid student id input in answer box.'
    }
    
  # kiem tra std_id co trong danh sach sinh vien
  stmt = select(Student).where(Student.id == student_id).exists().select()
  result = db.session.execute(stmt)
  if not result.scalar():
    return fail(
      data=[],
      message='Student id is not existed. Please contact the lecturer for this error.'
    )
    
  # save all files:
  time_now = timeNow()
  list_fileinfos = [] # (filename, filepath)
  for k in request.files.keys():
    file = request.files[k]
    filename = secure_filename(file.filename)
    filename = f'{time_now}_{student_id}_{filename}'
    filepath = os.path.join(FILE_SUBMISSION_PATH, filename)
    list_fileinfos.append((filename, filepath))
    file.save(filepath)
  
  # file info is ok, insert into database
  ## select assignment_id
  assignment = db.session.execute(db.select(Assignment).where(Assignment.name==assignment_name)).scalar_one()
  ## insert new submission
  list_filepaths = [x[1] for x in list_fileinfos]
  # print(list_fileinfos)
  sub = Submission(student_id=student_id, assignment_id=assignment.id, scores=[], files=list_filepaths)
  sub.save()
  
  # Cham bai vua nop
  jsondata = {
    "list_fileinfos": list_fileinfos,
    "student_id": str(student_id),
    "submission_id": str(sub.id)
  }
  requests.post(url=GRADER_URL, json=jsondata)
  
  # Tao Recommendation tam
  recr = Recommendation(status=1, submission_id=sub.id, list_testcase_id=[])
  recr.save()
  
  recr_id = recr.id
  encrypt_id = encrypt(recr_id)
  url = f'https://coderunner.codepractice.net/api/testcases/{encrypt_id}'
  recr.url = url
  recr.save()
  
  message = f'Link:\n{url}'
  
  # return success(
  #   data=[],
  #   message=message
  # )
  return message
  
@blueprint.route('/api/testcases/<encrypted_recr_id>', methods=['GET',])
def show_recommended_testcases(encrypted_recr_id):
  recr_id = decrypt(encrypted_recr_id)
  # recr = db.session.execute(select(Recommendation).where(Recommendation.id == recr_id)).first()
  recr = Recommendation.query.filter_by(id = recr_id).first()
  # print('hello', recr_id, recr.submission_id)
  # tìm student id
  # stu = db.session.execute(select(Submission).where(Submission.id == recr.submission_id)).first()
  sub = Submission.query.filter_by(id = recr.submission_id).first()
  student_id = sub.student_id
  
  if recr.status == 1:
    m = 'Hệ thống đang chấm điểm bài của bạn, vui lòng reload lại trang sau khoảng 3-5 phút'
  elif recr.status == 2:
    m = 'Hệ thống không còn testcases để bạn kiểm tra.'
  elif recr.status == 3:
    # m = 'Hiển thị kết quả gợi ý'
    m = None
  elif recr.status == 4:
    if recr.list_false_tcids is None:
      m = 'Bạn chưa làm đúng tất cả testcases của lần gợi ý trước. Bạn hãy nộp lại một lần làm bài mới để xem testcases làm sai.'
    else:
      list_false_tcids = [str(x) for x in recr.list_false_tcids]
      m = f'Bạn chưa làm đúng tất cả testcases của lần gợi ý trước.\nCác testcases sai là: {", ".join(list_false_tcids)}'
  elif recr.status == 5:
    m = 'Bạn đã đạt số lần gợi ý tối đa trong 1 ngày'
  else:
    m = 'Error'
  
  if m and recr.status != 4:
    return render_template('noti.html', student_id=student_id, message=m)
  else:
    if recr.status == 4:
      last_recr_status_3 = Recommendation.query.join(Submission, Recommendation.submission_id == Submission.id).filter(Submission.student_id == student_id).filter(Recommendation.status == 3).filter(Recommendation.updated_at < recr.updated_at).order_by(Recommendation.updated_at.desc()).first()
      # lấy dữ liệu các testcase lên từ lần Recommendation status == 3 gần nhất
      lids = last_recr_status_3.list_testcase_id
      message = m
    else:
      # lấy dữ liệu các testcase lên từ lần Recommend hiện tại
      lids = recr.list_testcase_id
      message = ''
    lfiles = []
    for id in lids:
      dic_t = {
        "id": id,
        # "input": readall(os.path.join('solution/workspace', f'tc{id}_input')),
        # "asclepius": readall(os.path.join('solution/workspace', f'tc{id}_asclepius_pack')),
        # "merlin": readall(os.path.join('solution/workspace', f'tc{id}_merlin_pack')),
        # "mushghost": readall(os.path.join('solution/workspace', f'tc{id}_mush_ghost')),
        "events": readall(os.path.join('solution/workspace', f'tc{id}_events')),
        "armyknights": readall(os.path.join('solution/workspace', f'tc{id}_armyknights')),
        "expect": readall(os.path.join('solution/workspace', f'output{id}')),
      }
      lfiles.append(dic_t)
    # message = m if m is not None else ''
    return render_template('rec.html', student_id=student_id, lfiles=lfiles, message=message)
  return success()

@blueprint.route('/api/internalrecommend', methods=['POST',])
def internal_recommend():
  @copy_current_request_context
  def thread_recommend(dic_data):
    submission_id = dic_data['submission_id']
    student_id = str(dic_data['student_id'])
    
    # Note: kiem tra nếu kết quả chấm là đúng tất cả lần recommend trước thì mới thực hiện recommend
    # thông báo kết quả này trên trang web như thế nào? dùng bảng recommendation được ko? - được: dùng status = 4
    pass_all = True
    list_false_tcids = []
    
    # last_r = Recommendation.query.filter(Recommendation.status == 3).order_by(Recommendation.updated_at.desc()).first()
    last_r = Recommendation.query.join(Submission, Recommendation.submission_id == Submission.id).filter(Submission.student_id == student_id).filter(Recommendation.status == 3).order_by(Recommendation.updated_at.desc()).first()
    
    if last_r:
      # kiểm tra thử đúng hết tất cả testcase trong last_recommendation không?
      sub = Submission.query.filter(Submission.id == submission_id).order_by(Submission.updated_at.desc()).first()
      
      list_rtcids = last_r.list_testcase_id
      # print(type(Clist_testcase_ids[0]), type(list_rtcids[0]), list_rtcids[0])
      for tcid in list_rtcids:
        idx = Clist_testcase_ids.index(tcid)
        print(student_id, tcid, idx, sub.scores[idx], flush=True) # in để debug
        if sub.scores[idx] == False:
          list_false_tcids.append(tcid)
          pass_all = False
          # break # comment để debug
        
    if not pass_all:
      r = Recommendation.query.filter(Recommendation.submission_id == submission_id).first()
      r.status = 4
      r.list_false_tcids = list_false_tcids
      r.save()
      
      return fail(message='not full pass previous recommended testcases')
      
    
    # Note: kiểm tra nếu trong ngày hôm nay đã có 5 lần req rồi thì không đưa ra gợi ý, status = 5
    today = date.today()
    start = datetime.combine(today, time=time(0,0,0))
    # list_recommendation = Recommendation.query.filter(Recommendation.status == 3).filter(Recommendation.updated_at >= start).order_by(Recommendation.updated_at.desc()).all()
    list_recommendation = Recommendation.query.join(Submission, Recommendation.submission_id == Submission.id).filter(Submission.student_id == student_id).filter(Recommendation.status == 3).filter(Recommendation.updated_at >= start).order_by(Recommendation.updated_at.desc()).all()
    if len(list_recommendation) >= 5:
      r = db.session.execute(db.select(Recommendation).where(Recommendation.submission_id==submission_id)).scalar_one()
      r.status = 5
      r.save()
      
      return fail(message='limit number of request: 5')
    
    sub = Submission.query.filter(Submission.id == submission_id).order_by(Submission.updated_at.desc()).first()

    # bắt đầu gợi ý
    submission_id = dic_data['submission_id']
    student_id = str(dic_data['student_id'])
    
    assignment_id = sub.assignment_id
      
    if student_id in rec_apr1:
      recommendation_2(submission_id, assignment_id, student_id)
    elif student_id in rec_apr2:
      recommendation_3(submission_id, assignment_id, student_id)
    elif student_id in rec_apr3:
      recommendation_4(submission_id, assignment_id, student_id)
    else:
      print('Error')
      assert(False)
  
  dic_data = {
    "list_fileinfos": request.json.get('list_fileinfos'),
    "student_id": str(request.json.get('student_id')),
    "submission_id": request.json.get('submission_id')
  }
  # thread = threading.Thread(target=thread_recommend, args=(dic_data,))
  thread = LimitThread(target=thread_recommend, args=(dic_data,))
  # thread.daemon = True
  thread.start()
  
  return success()