from flaskr.database import db
from sqlalchemy import Column, Boolean, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func

import uuid

class StudentOnAssignment(db.Model):
  __tablename__ = 'student_on_assignments'
  
  id = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
  is_active = Column(Boolean, default=True)
  created_at = Column(DateTime(timezone=True), default=func.now())
  updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=db.func.now())
  
  student_id = Column(UUID(as_uuid=True), ForeignKey('students.id'), nullable=False)
  assignment_id = Column(UUID(as_uuid=True), ForeignKey('assignments.id'), nullable=False)

  __table_args__ = (
    UniqueConstraint('student_id', 'assignment_id', name='student_id_assignment_id'),
  )
  
  def __str__(self):
    s = [
      f'id = {self.id}',
      f'student_id = {self.student_id}',
      f'assignment_id = {self.assignment_id}'
    ]
    s = ', '.join(s)
    s = f'StudentOnAssignment[{s}]'
    return s