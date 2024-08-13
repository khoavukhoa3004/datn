from flask import Blueprint, request
from flaskr.domain.account import account_services
from flaskr.domain.assignment.assignment_teacher_models import TeacherOnAssignment
from flaskr.domain.submission.submission_models import Submission
from flaskr.domain.student.student_models import Student
from flaskr.domain.assignment.assignment_student_models import StudentOnAssignment
from flaskr.domain.assignment.assignment_services import AssignmentService
from flaskr.domain.teacher.teacher_models import Teacher
from flaskr.domain.recsys.recsys_models import Recommendation
from flaskr.utils.exceptions import BadRequestException, NotFoundException
from flaskr.domain.account.account_services import AccountService, Account
from flaskr.utils.base_response import BaseResponse
import requests
from email_validator import validate_email, EmailNotValidError
from constants import FILE_SUBMISSION_PATH, GRADER_URL
from flaskr.domain.assignment.assignment_models import Assignment
import time
from datetime import datetime, timezone
import os
import csv


date_format = date_format ='%Y-%m-%dT%H:%M:%S.%fZ' # The format of the date string


class AssignmentController:
  assignment_controller = Blueprint('assignment_controller', __name__)
  
  @classmethod
  @assignment_controller.route('/api/assignments', methods=['POST'])
  @AccountService.authenticate
  def create_assignment():
    '''
    TEACHER
    '''
    account = request.account
    if account.type.name == 'STUDENT':
      raise BadRequestException('PERMISSION_DENIED')
    body = request.get_json()
    if not 'name' in body:
      raise BadRequestException('NAME_IS_NOT_FOUND')
    if (not 'start_date' in body) or (not 'end_date' in body):
      raise BadRequestException('DEADLINE_IS_NOT_FOUND')
    try:
      start_date = datetime.strptime(request.json.get('start_date'), date_format)
      end_date = datetime.strptime(request.json.get('end_date'), date_format)
    except ValueError:
      raise BadRequestException('TIME_VALUE_ERROR')
    
    teacher = Teacher.query.filter_by(account_id=account.id).first()
    AssignmentService.create(request.json.get('name'), start_date, end_date, teacher.id, request.json.get('description'))
    return BaseResponse.ok()
  
  @classmethod
  @assignment_controller.route('/api/assignments', methods=['GET'])
  @AccountService.authenticate
  def get_list():
    '''
    TEACHER & STUDENT
    '''
    return BaseResponse.of(AssignmentService.get_list(request.account))

  @classmethod
  @assignment_controller.route('/api/assignments/<string:id>/submission', methods=['POST'])
  @AccountService.authenticate
  @AccountService.verify_student
  def create_submission(id):
    '''
    STUDENT
    '''
    assignment = StudentOnAssignment.query \
      .join(Assignment, Assignment.id == StudentOnAssignment.assignment_id) \
      .filter(StudentOnAssignment.assignment_id == id, StudentOnAssignment.student_id == request.student.id) \
      .with_entities(
        Assignment.end_date,
      ).first()
    if not assignment:
      raise NotFoundException('STUDENT_NOT_FOUND')
    
    # TODO Need to fix timezone
    # print(datetime.now(timezone.utc))
    current_time = datetime.now(timezone.utc)
    if current_time > assignment[0]:
      raise BadRequestException('DEADLINE_MISSES')
    if 'files[]' not in request.files:
      return NotFoundException('FILES_NOT_FOUND')
    
    files = request.files.getlist('files[]')
    file_paths_2 = []
    folder_path = f'/root/sys/TRS/files/test'
    folder_path_2 = f'/app/files/test'
    folder_path = folder_path_2 #Dong cmt de cham port 5005
    # folder_path_2 = folder_path
    for file in files:  
      os.makedirs(folder_path, exist_ok=True)
      
      current_path = os.path.join(folder_path, f'{request.student.mssv}-{current_time.strftime("%Y-%m-%dT%H-%M-%S")}-{file.filename}')
      current_path_2 = os.path.join(folder_path_2, f'{request.student.mssv}-{current_time.strftime("%Y-%m-%dT%H-%M-%S")}-{file.filename}')
      
      file.save(current_path)
      file_paths_2.append(current_path_2)
    # print('File path ne', file_paths)

    submission = Submission(student_id=request.student.id, assignment_id=id, files=file_paths_2)
    submission.save()

    std_id = request.student.mssv

    # Cham bai vua nop
    jsondata = {
      "list_fileinfos": file_paths_2,
      "student_id": str(std_id),
      "submission_id": str(submission.id)
    }

    print(jsondata)

    recr = Recommendation(status=1, submission_id=submission.id, list_testcase_id=[])
    recr.save()
    received_response = False

    requests.post(url=GRADER_URL, json=jsondata)
    # while not received_response:
    #   try:
    #       response = requests.post(url=GRADER_URL, json=jsondata)
          
    #       # Kiểm tra xem response có thành công không
    #       if response.status_code == 200:
    #           print('SUCCESS')
    #           received_response = True
    #       else:
    #           # Thử lại sau một khoảng thời gian nếu request không thành công
    #           print("Request không thành công. Status code:", response.status_code)
    #           time.sleep(5)  # Chờ 5 giây trước khi thử lại
    #   except Exception as e:
    #       # Xử lý các lỗi xảy ra trong quá trình gửi yêu cầu
    #       print("Lỗi:", str(e))
    #       time.sleep(5)  # Thử lại sau một khoảng thời gian
    
    # Tao Recommendation tam

    return BaseResponse.ok()
  
  @classmethod
  @assignment_controller.route('/api/assignments/<string:id>/assign-students', methods=['POST'])
  @AccountService.authenticate
  @AccountService.verify_teacher
  def assign_multiple_student(id):
    assignment = Assignment.query.filter_by(author_id=request.teacher.id)
    if not assignment:
      raise BadRequestException('PERMISSION_DENIED')
    files = request.files.getlist('files[]')
    for file in files:
      csv_data = file.read().decode('utf-8')
      reader = csv.reader(csv_data.splitlines(), delimiter=',')
      next(reader)
      reader = list(reader)
      for row in reader:
        try:
          print('name', row[1] + ' ' + row[2])
          print('mssv', row[3])
          print('mssv', row[0])
          status, student = AccountService.create_account((row[1] + ' ' + row[2]), row[3], 'STUDENT', row[0])
          if status in ['EXIST_STUDENT', 'STUDENT']:
            print('student ne', student)
            student_on_assignment = StudentOnAssignment(student_id=student.id, assignment_id=id)
            print('oke')
            student_on_assignment.save()
        except Exception as e:
          print('row error:', row)
          print('error: ', str(e))
    return BaseResponse.ok()
    
  
  @classmethod
  @assignment_controller.route('/api/assignments/<string:id>', methods=['PATCH'])
  @AccountService.authenticate
  @AccountService.verify_teacher
  def assign_student(id):
    '''
    TEACHER
    '''
    assignment = Assignment.query.filter_by(id=id).first()
    if not assignment:
      raise BadRequestException('ASSIGNMENT_NOT_FOUND')
    if request.account.type.name == 'STUDENT':
      raise BadRequestException('PERMISSION_DENIED')
    ids = request.json.get('ids', [])
    if ids and len(ids) > 0: 
      existing_ids = list(map(lambda x: str(x.id), Student.query.filter(Student.id.in_(ids)).all()))
      not_found_list = list(set(ids) - set(existing_ids))
      for id in existing_ids:
        student_on_assignment = StudentOnAssignment(student_id=id, assignment_id=assignment.id)
        student_on_assignment.save()
    if request.json.get('description'):
      assignment.description = request.json.get('description')
    if request.json.get('name'):
      assignment.name = request.json.get('name')
    assignment.save()  
    return BaseResponse.of({'not_found_list': not_found_list}) 
  
  @classmethod
  @assignment_controller.route('/api/assignments/<string:id>', methods=['GET'])
  @AccountService.authenticate
  def get_detail_student(id):
    '''
    TEACHER & STUDENT
    #TODO: Currently, we combine get detail assignment, get list student and get list teacher into 1 api (NEED TO SEPARATE THEM LATER)
    #TODO: Refactor code
    '''
    return BaseResponse.of(AssignmentService.get_detail_student(id, request.account)) 

  @classmethod
  @assignment_controller.route('/api/assignments/<string:id>/collaborators', methods=['POST'])
  @AccountService.authenticate
  @AccountService.verify_teacher
  def add_teacher_on_assignment(id):
    '''
    TEACHER
    '''
    assignment = Assignment.query.filter_by(author_id=request.teacher.id).first()
    if assignment == None:
      raise BadRequestException('PERMISSION_DENIED')
    try:
      email = validate_email(request.json.get('email')).email
      AssignmentService.add_teacher_on_assignment(id, assignment.author_id, email, request.json.get('name'))
    except EmailNotValidError:
      raise BadRequestException('EMAIL_NOT_VALID')
    return BaseResponse.ok()