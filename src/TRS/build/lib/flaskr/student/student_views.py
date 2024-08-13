import logging
from flask import Blueprint, request, Response
from flask.globals import current_app
from flask.json import jsonify
from flaskr.utils.file import File
from constants import FILE_LIST_STUDENTS_PATH
from werkzeug.utils import secure_filename
import os
from flaskr.utils.time import timeNow
from flaskr.student.student_models import Student
import pandas as pd

blueprint = Blueprint('student', __name__)

@blueprint.route('/api/students', methods=['POST',])
def update_student_list():
  if len(request.files.keys()) != 1:
    return 'Number of upload files is invalid'
  
  key = 'liststudents'
  file = request.files[key]
  
  if file.filename[-5:] != '.xlsx':
    return 'Only support file of type xlsx'
  
  time_now = timeNow()
  filename = secure_filename(file.filename)
  filename = f'{time_now}_{filename}'
  filepath = os.path.join(FILE_LIST_STUDENTS_PATH, filename)
  file.save(filepath)
  
  df = pd.read_excel(filepath)
  for idx, row in df.iterrows():
    id = row['ID number']
    email = row['Email address']
    s = Student(id=id, email=email)
    s.save()
  
  return 'Upload successfully'