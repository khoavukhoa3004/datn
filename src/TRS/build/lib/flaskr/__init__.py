import os, sys
from flask import Flask, request
from flask.globals import current_app
from flaskr.extensions import db
import logging
from datetime import date
import pandas as pd
from dotenv import load_dotenv
from flask_cors import CORS
from config.config import DevelopmentConfig
from constants import DB_INIT
from apscheduler.schedulers.background import BackgroundScheduler
# from flaskr.matrixfactorization.MF_views import buildMF, exportInitMF
from flaskr.tcclassification.tcclassification_views import buildClassification

'''
Note: for create table, uncomment following code
'''
from flaskr.assignment.assignment_models import Assignment
from flaskr.submission.submission_models import Submission

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

    if app.config.get('INIT_DB'):
        with app.app_context():
            pass
      
    with app.app_context():
      schedule = BackgroundScheduler(deamon=True)
      # schedule.add_job(buildMF, 'cron', args=[app], id='buidMF', hour=0, minute=0) # 7 - 00
      schedule.add_job(buildClassification, 'cron', args=[app], id='buidTcClassification', hour=0, minute=0) # 7 - 00
      # schedule.add_job(buildClassification, 'interval', args=[app], id='buidTcClassification', seconds=1) # for testing
      schedule.start()
    
    from datetime import datetime, timedelta
    now = datetime.now()
    print("Current Time =", now, f'Time + 7: {now + timedelta(hours=7)}')
    
    return app

def register_blueprints(app):
  from flaskr.hello.hello_views import blueprint as HelloBP
  app.register_blueprint(HelloBP)
  from flaskr.recsys.recsys_views import blueprint as RecBP
  app.register_blueprint(RecBP)
  from flaskr.student.student_views import blueprint as StudentBP
  app.register_blueprint(StudentBP)
  from flaskr.assignment.assignment_views import blueprint as AssignmentBP
  app.register_blueprint(AssignmentBP)
  pass

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