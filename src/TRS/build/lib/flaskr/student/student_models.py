from flaskr.database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import CheckConstraint
import uuid

class Student(db.Model):
  __tablename__ = 'students'
  
  id = db.Column(db.String, unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
  email = db.Column(db.String, unique=True, nullable=False)
  
  def __str__(self) -> str:
    s = [
      f'id = {self.id}',
      f'email = {self.email}'
    ]
    s = ', '.join(s)
    s = f'Student[{s}]'
    return s