from flaskr.database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import CheckConstraint, Column, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
import uuid
import enum

class SubmissionStatus(enum.Enum):
  WAITING = 'WAITING'
  FAILED = 'FAILED'
  SUCCESS = 'SUCCESS'

class Submission(db.Model):
  __tablename__ = 'submissions'
  
  # id
  id = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
  student_id = Column(UUID(as_uuid=True),ForeignKey('students.id'),  nullable=False)
  assignment_id = Column(UUID(as_uuid=True), ForeignKey('assignments.id'), unique=False, nullable=False)
  # array of multiple testcase with pass/fail = 1/0
  # each number of testcase is differenct from assignments
  status = Column(Enum(SubmissionStatus), nullable=False, default=SubmissionStatus.WAITING)
  scores = Column(ARRAY(db.Boolean), unique=False, nullable=False)
  files = Column(ARRAY(db.String), unique=False, nullable=False)
  form = relationship("Form", back_populates="submission", uselist=False)
  
  recommendation = relationship("Recommendation", back_populates="submission", uselist=False)

  def __str__(self) -> str:
    s = [
      f'student_id = {self.student_id}',
      f'assignment_id = {self.assignment_id}',
      f'scores = {self.scores}'
    ]
    s = ', '.join(s)
    s = f'Submission[{s}]'
    return s