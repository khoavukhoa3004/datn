import logging
from flask import Blueprint, request, Response
from flask.globals import current_app
from flask.json import jsonify
from flaskr.utils.file import File
from constants import FILE_LIST_STUDENTS_PATH
from werkzeug.utils import secure_filename
import os
from flaskr.utils.time import timeNow
from flaskr.assignment.assignment_models import Assignment
import pandas as pd

blueprint = Blueprint('assignment', __name__)
@blueprint.route('/api/assignment', methods=['POST',])
def create_assignment():
  body = request.get_json()
  if not 'name' in body:
    return 'name does not existed'
  
  name = body['name']
  a = Assignment(name=name)
  a.save()
  
  return 'Create successfully'