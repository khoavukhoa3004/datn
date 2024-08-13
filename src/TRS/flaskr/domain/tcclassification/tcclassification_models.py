from flaskr.database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY

class TcClassification(db.Model):
  __tablename__ = 'tcclassification'
  
  list_testcase_ids = db.Column(ARRAY(db.Integer), unique=False, nullable=False)
  
  # level: 1-de, 2-TB, 3-Kho
  list_testcase_levels = db.Column(ARRAY(db.Integer), unique=False, nullable=False)
  
  assignment_id = db.Column(UUID(as_uuid=True), unique=False, nullable=False)
  
  silhouette_score = db.Column(db.Float, unique=False, nullable=True)
  
  def __str__(self) -> str:
    s = [
      f'list_testcase_ids = {self.list_testcase_ids}',
      f'list_testcase_levels = {self.list_testcase_levels}',
      f'assignment_id = {self.assignment_id}'
    ]
    s = ', '.join(s)
    s = f'TcClassification[{s}]'
    return s