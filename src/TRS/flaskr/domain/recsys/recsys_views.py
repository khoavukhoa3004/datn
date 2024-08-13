
import os
from datetime import date, time, datetime
from sqlalchemy import not_

from flask import Blueprint, request
from flask import copy_current_request_context
from flaskr.utils.base_response import BaseResponse
from flaskr.utils.exceptions import BadRequestException, NotFoundException
from flaskr.domain.account.account_services import AccountService
from flaskr.database import db
from flaskr.domain.student.student_models import Student
from flaskr.domain.submission.submission_models import Submission
from flaskr.domain.recsys.recsys_models import Recommendation
from flaskr.domain.recsys.algorithm import recommendation_1, recommendation_2, recommendation_3, recommendation_4
from flaskr.utils.file import readall
from flaskr.utils.limitthread import LimitThread

from constants.constants import rec_apr1, rec_apr2, rec_apr3, list_testcase_ids as Clist_testcase_ids
from response import success, fail

blueprint = Blueprint('recsys', __name__)

@blueprint.route('/api/testcases/previous', methods=['GET'])
@AccountService.authenticate
@AccountService.verify_student
def get_previous_recommendation_submission():
  submission_id = request.args.get('submission_id')
  submission = Submission.query.filter_by(id=submission_id, student_id=request.student.id).first()
  if not submission:
    raise NotFoundException('SUBMISSION_NOT_FOUND')
  current_recommendation = Recommendation.query.filter_by(submission_id=submission_id, ).first()
  if (not current_recommendation):
    raise BadRequestException('INVALID_SUBMISSION_ID')
  if(current_recommendation.status != 3 and current_recommendation.status != 2):
    return BaseResponse({
      'last_submission_id': None,
      'is_filled': True, 
      'files': [], 
      'status': None},'').to_response()

  last_recommendation = (Recommendation.query
      .join(Submission, Submission.id == Recommendation.submission_id)
      .join(Student, Student.id == Submission.student_id)
      .order_by(Recommendation.created_at.desc())
      .filter(
        Student.id == request.student.id, 
        not_(Submission.id == submission_id), 
        Recommendation.is_filled_form == False,
        (Recommendation.status == 3),
        Recommendation.updated_at < current_recommendation.updated_at
        )
      .with_entities(
        Submission.id, 
        Recommendation.list_testcase_id,
        Recommendation.status,
        )
      .first())
  if not last_recommendation:
    return BaseResponse({
      'last_submission_id': None,
      'is_filled': True, 
      'files': [], 
      'status': None},'').to_response()
  results = []
  for id in last_recommendation[1]:
    dic_t = {
      "id": id,
      "events": readall(os.path.join('solution/workspace', f'tc_{id}.cpp')),
      "expect": readall(os.path.join('solution/workspace', f'tc_{id}.out')),
    }
    results.append(dic_t)
  return BaseResponse.of({
    'last_submission_id': last_recommendation[0],
    'is_filled': False,
    'files': results,
    'status': last_recommendation[2],
  });
  
@blueprint.route('/api/testcases', methods=['GET'])
@AccountService.authenticate
@AccountService.verify_student
def show_recommended_testcases():
  sub_id = request.args.get('submission_id')
  # try:
  #   recr = Recommendation.query.filter_by(submission_id = sub_id).first()
  #   print('recommend', recr)
  #   if not recr:
  #     return  BaseResponse({
  #       "files": [],
  #       "status": None,
  #     }, None).to_response()
  # except:
  #   return BaseResponse({
  #       "files": [],
  #       "status": None,
  #     }, None).to_response()
  submission = Submission.query.filter_by(id=sub_id, student_id=request.student.id).first()
  if not submission:
    raise NotFoundException('SUBMISSION_NOT_FOUND')
  recr = Recommendation.query.filter_by(submission_id = sub_id).first()

  std_id = request.student.mssv

  std = Student.query.filter_by(mssv=std_id).first()
  
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
    return fail (
      message=m
    )
  else:
    if recr.status == 4:
      lids = recr.list_false_tcids
      print('lids', lids)
    else:
      # lấy dữ liệu các testcase lên từ lần Recommend hiện tại
      lids = recr.list_testcase_id
      m = ''
    lfiles = []
    for id in lids:
      dic_t = {
        "id": id,
        "events": readall(os.path.join('solution/workspace', f'tc_{id}.cpp')),
        "expect": readall(os.path.join('solution/workspace', f'tc_{id}.out')),
      }
      lfiles.append(dic_t)
    # message = m if m is not None else ''
  return BaseResponse({
    "files": lfiles,
    "status": recr.status,
  }, m).to_response()

@blueprint.route('/api/internalrecommend', methods=['POST',])
def internal_recommend():
  @copy_current_request_context
  def thread_recommend(dic_data):
    submission_id = dic_data['submission_id']
    student_id = str(dic_data['student_id'])
    print('dic data: ', dic_data)
    
    # Note: kiem tra nếu kết quả chấm là đúng tất cả lần recommend trước thì mới thực hiện recommend
    # thông báo kết quả này trên trang web như thế nào? dùng bảng recommendation được ko? - được: dùng status = 4
    pass_all = True
    list_false_tcids = []
    
    student = Student.query.filter_by(mssv=student_id).first()
    # last_r = Recommendation.query.filter(Recommendation.status == 3).order_by(Recommendation.updated_at.desc()).first()
    last_r = (Recommendation.query
                          .join(Submission, Recommendation.submission_id == Submission.id)
                          .filter(Submission.student_id == student.id)
                          .filter(Recommendation.status == 3)
                          .order_by(Recommendation.updated_at.desc()).first())

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
      print('r', r)
      r.status = 4
      r.list_false_tcids = list_false_tcids
      r.save()
      return fail(message='not full pass previous recommended testcases')
    
    # Note: kiểm tra nếu trong ngày hôm nay đã có 5 lần req rồi thì không đưa ra gợi ý, status = 5
    today = date.today()
    start = datetime.combine(today, time=time(0,0,0))
    # list_recommendation = Recommendation.query.filter(Recommendation.status == 3).filter(Recommendation.updated_at >= start).order_by(Recommendation.updated_at.desc()).all()
    list_recommendation = (Recommendation.query
      .join(Submission, Recommendation.submission_id == Submission.id)
      .filter(Submission.student_id == student.id)
      .filter(Recommendation.status == 3)
      .filter(Recommendation.updated_at >= start)
      .order_by(Recommendation.updated_at.desc())
      .all())
    if len(list_recommendation) >= 5:
      r = db.session.execute(db.select(Recommendation).where(Recommendation.submission_id==submission_id)).scalar_one()
      r.status = 5
      r.save()
      
      return fail(message='limit number of request: 5')
    
    # bắt đầu gợi ý
    submission_id = dic_data['submission_id']
    student_id = str(dic_data['student_id'])

    sub = (Submission.query
      .filter(Submission.id == submission_id)
      .order_by(Submission.updated_at.desc())
      .first())
    assignment_id = sub.assignment_id
      
    if student_id in rec_apr1:
      print('recommendation_2')
      recommendation_2(submission_id, assignment_id, student_id)
    elif student_id in rec_apr2:
      print('recommendation_3')
      recommendation_3(submission_id, assignment_id, student_id)
    elif student_id in rec_apr3:
      print('recommendation_4')
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