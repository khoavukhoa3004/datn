import os, sys
import logging
from datetime import date
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, request
from flask.globals import current_app
from flaskr.extensions import db
from flask_cors import CORS
from config.config import DevelopmentConfig
from constants import DB_INIT
from apscheduler.schedulers.background import BackgroundScheduler
# from flaskr.tcclassification.tcclassification_views import buildClassification

'''
Note: for create table, uncomment following code
'''
from flaskr.domain.account.account_models import Account
from flaskr.domain.student.student_models import Student
from flaskr.domain.teacher.teacher_models import Teacher
from flaskr.domain.assignment.assignment_models import Assignment
from flaskr.domain.assignment.assignment_student_models import StudentOnAssignment
from flaskr.domain.assignment.assignment_teacher_models import TeacherOnAssignment
from flaskr.domain.matrixfactorization.MF_models import MatrixFactorization
from flaskr.domain.form.form_models import Form
from flaskr.domain.submission.submission_models import Submission
from flaskr.domain.recsys.recsys_models import Recommendation

from flaskr.domain.matrixfactorization.MF_views import buildRSVD, buildTimeSVD, exportInitMF, buildLSTM

# utils
from flaskr.utils.base_response import BaseResponse
from flaskr.utils.exceptions import *
# constants
from constants import *
PATH_SEP = os.path.sep

sys.path.append(os.path.join(os.getcwd(), 'flaskr'))
sys.path.append(os.path.join(os.getcwd(), 'config'))
sys.path.append(os.path.join(os.getcwd(), 'constants'))
load_dotenv()

# log to file
if os.getenv('FLASK_ENV') == 'production':
    logging.basicConfig(level=os.getenv('LOGGING_LEVEL'))

elif os.getenv('FLASK_ENV') == 'development':
    logging.basicConfig(stream=sys.stdout, level=os.getenv('LOGGING_LEVEL'))

def test():
  from datetime import date, timedelta, time, datetime
  today = date.today()
  pre_date = today + timedelta(days=-1)
  start = datetime.combine(pre_date, time=time(0,0,0))
  end = datetime.combine(today, time=time(0,0,0))
  start = datetime(2023, 3, 9, 0, 0, 0)
  end = datetime(2023, 3, 10, 0, 0, 0)
  student_id = '2213332'
  list_recommendation = Recommendation.query.join(Submission, Recommendation.submission_id == Submission.id).filter(Submission.student_id == student_id).filter(Recommendation.status == 3).filter(Recommendation.updated_at >= start).filter(Recommendation.updated_at <= end).order_by(Recommendation.updated_at.desc()).all()
  print(f'start: {start}, end: {end}')
  print(f'len(list_recommendation): {len(list_recommendation)}')

def create_app(test_config=None):
    app = Flask(__name__, template_folder='../templates', instance_relative_config=True)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    cors = CORS(app)

    if os.getenv('FLASK_ENV') == 'production':
        config_flask_logger(app)
        
    if test_config is None:
      app.config.from_object(DevelopmentConfig)
    else:
      app.config.from_mapping(test_config)

    db.init_app(app)

    with app.app_context():
      if DB_INIT:
        db.create_all()
    register_blueprints(app)
    register_exception(app)

    if app.config.get('INIT_DB'):
        with app.app_context():
            pass
      
    with app.app_context():
      # buildRSVD(app)
      # buildTimeSVD(app)
      # buildLSTM(app)
      schedule = BackgroundScheduler(deamon=True)
      schedule.add_job(buildRSVD, 'cron', args=[app], id='buidRSVD', hour=19, minute=0) # 7 - 00
      schedule.add_job(buildTimeSVD, 'cron', args=[app], id='buidTimeSVD', hour=19, minute=0) # 7 - 00
      schedule.add_job(buildLSTM, 'cron', args=[app], id='buidLSTM', hour=19, minute=0) # 7 - 00
      schedule.start()
      pass
    
    from datetime import datetime, timedelta
    now = datetime.now()
    print("Current Time =", now, f'Time + 7: {now + timedelta(hours=7)}')
    
    return app

def register_blueprints(app):
  from flaskr.domain.account.account_controllers import AccountController
  app.register_blueprint(AccountController.account_controller)
  from flaskr.domain.assignment.assignment_controllers import AssignmentController
  app.register_blueprint(AssignmentController.assignment_controller)
  from flaskr.domain.submission.submission_controllers import SubmissionController
  app.register_blueprint(SubmissionController.submission_controller)
  from flaskr.domain.recsys.recsys_views import blueprint as RecBP
  app.register_blueprint(RecBP)
  from flaskr.domain.student.student_controllers import StudentController
  app.register_blueprint(StudentController.student_controller)
  from flaskr.domain.form.form_controllers import FormController
  app.register_blueprint(FormController.form_controller)
  pass

def register_exception(app):
  app.register_error_handler(ForbiddenResourceException, CustomExceptionHandler().handle_forbidden_resource)
  app.register_error_handler(MiddlewareException, CustomExceptionHandler().handle_middlewares)
  app.register_error_handler(BadRequestException, CustomExceptionHandler().handle_bad_request_exception)
  app.register_error_handler(NotFoundException, CustomExceptionHandler().handle_not_found_exception)
  app.register_error_handler(InternalServerException, CustomExceptionHandler().handle_internal_server_exception)


def seed_exer_ques_level(file_path=f'data{PATH_SEP}KTLT_questions_with_level.csv'):
    df = pd.read_csv(file_path)
    for idx, row in df.iterrows():
        ques_id = row['question_id']
        level = row['label']
        query = f"""
        update questions
        set level = {level}
        where id = '{ques_id}'
        """
def config_flask_logger(app):
    log_file_path = f"logs{PATH_SEP}{date.today().strftime('%d-%m-%Y')}.log"
    if not os.path.exists(log_file_path):
        open(log_file_path, 'w')
        
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(os.getenv('LOGGING_LEVEL'))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    app.logger.setLevel(os.getenv('LOGGING_LEVEL'))
    app.logger.addHandler(fh)

    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(os.getenv('LOGGING_LEVEL'))
    werkzeug_logger.addHandler(fh)

def register_database(app, db):
  db.init_app(app)