from flaskr.domain.teacher.teacher_models import Teacher
from flaskr.utils.exceptions import ForbiddenResourceException
# from flaskr.config import SECRET_KEY
from flaskr.domain.account.response.account_response import AccountResponse
from flaskr.domain.student.student_models import Student
from flaskr.domain.account.account_models import Account
from flask import request, jsonify, abort
from functools import wraps
from google.oauth2 import id_token
from google.auth.transport import requests
from email_validator import validate_email, EmailNotValidError

import time

class AccountService:
  # TODO Create access token riêng, không phụ thuộc vào Google
  # TODO Vì Account google expire sau 1 tiếng
  # @staticmethod
  # def generate_access_token(account_id, email: str, type):
  #   # Define the expiration time for the access token (1 day from now)
  #   expiry = datetime.utcnow() + timedelta(days=1)

  #   # Create the payload for the access token
  #   payload = {
  #       'uid': str(account_id),
  #       'email': email,
  #       'type': str(type),
  #       'exp': expiry
  #   }
  #   # Sign the access token using a secret key
  #   secret_key = SECRET_KEY
  #   access_token = jwt.encode(payload, secret_key, algorithm='HS256')
  #   return access_token
  
  @staticmethod
  def verify_token(token: str):
    try:
      idinfo = id_token.verify_oauth2_token(token, requests.Request())
      if idinfo['exp'] < time.time():
        raise ForbiddenResourceException('TOKEN_EXPIRED')
      email = validate_email(idinfo['email']).email
      account = Account.query.filter_by(email = email, is_active=True).first()
      if not account:
        raise ForbiddenResourceException('EMAIL_NOT_FOUND')
      return account
    except EmailNotValidError:
      raise ForbiddenResourceException('EMAIL_NOT_VALID')
    except ValueError:
      raise ForbiddenResourceException('INVALID_TOKEN')

  
  @staticmethod
  def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      auth_header = request.headers.get('Authorization')
      if auth_header and auth_header.startswith('Bearer'):
        token = auth_header.split(' ')[1]
        request.account = AccountService.verify_token(token)
        return func(*args, **kwargs)
      else:
        raise ForbiddenResourceException('INVALID_TOKEN')
    return wrapper

  @staticmethod
  def verify_teacher(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      if request.account.type.name != 'TEACHER':
        raise ForbiddenResourceException('PERMISSION_DENIED')
      teacher = Teacher.query.filter_by(id=request.account.teacher.id).first()
      request.teacher = teacher
      return func(*args, **kwargs)
    return wrapper


  @staticmethod
  def verify_student(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      if request.account.type.name != 'STUDENT':
        raise ForbiddenResourceException('PERMISSION_DENIED')
      student = Student.query.filter_by(id=request.account.student.id).first()
      request.student = student
      return func(*args, **kwargs)
    return wrapper

        
  @staticmethod
  def create_account(name, email, type, mssv=None):
    exist_account = Account.query.filter_by(email=email).first()
    if exist_account:
      if exist_account.type.name == 'TEACHER':
        teacher = Teacher.query.filter_by(account_id=exist_account.id).first()
        return 'EXIST_TEACHER', teacher
      else:
        student = Student.query.filter_by(account_id=exist_account.id).first()
        return 'EXIST_STUDENT', student
    account = Account(name, email, type)
    account.save()
    if type == 'STUDENT':
      student = Student(account_id=account.id, mssv=mssv)
      student.save()
      student = Student.query.filter_by(account_id=account.id).first()
      return 'STUDENT', student
    elif type == 'TEACHER':
      teacher = Teacher(account_id=account.id)
      teacher.save()
      teacher = Teacher.query.filter_by(account_id=account.id).first()
      return 'TEACHER', teacher
    
  @staticmethod
  def get_detail(account_id) -> AccountResponse:
    account = Account.query.filter_by(id=account_id).with_entities(Account.name, Account.email, Account.created_at, Account.type).first()
    if not account:
      return jsonify({'error': 'The account is not exist'}), 404
    return jsonify({ 'data': account}), 200

