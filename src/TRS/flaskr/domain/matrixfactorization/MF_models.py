from flaskr.database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import ARRAY
import numpy as np

class   MatrixFactorization(db.Model):
  __tablename__ = 'matrixfactorization'
  
  # id
  list_student_ids = db.Column(ARRAY(db.String), unique=False, nullable=False)
  list_testcase_ids = db.Column(ARRAY(db.Integer), unique=False, nullable=False)
  
  assignment_id = db.Column(UUID(as_uuid=True), unique=False, nullable=False)
  model_name = db.Column(db.String, unique=False, nullable=False)
  # matrix.shape = (students, testcases)
  # matrix = db.Column(ARRAY(db.Float, dimensions=2), unique=False, nullable=False)
  matrix_npz_path = db.Column(db.String, unique=False, nullable=False)
  
  def __str__(self) -> str:
    s = [
      f'list_student_ids = {self.list_student_ids}',
      f'list_testcase_ids = {self.list_testcase_ids}',
      f'assignment_id = {self.assignment_id}',
      f'model_name = {self.model_name}',
      f'matrix_npz_path = {self.matrix_npz_path}'
    ]
    s = ', '.join(s)
    s = f'MF[{s}]'
    return s
  
def saveMatrix(m, path):
  np.savez(file=path, matrix=m, allow_pickle=True) # matrix: hard-code
  
def loadMatrix(path):
  npz = np.load(path, allow_pickle=True)
  m = npz['matrix']
  return m