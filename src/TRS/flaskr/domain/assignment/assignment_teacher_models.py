from flaskr.database import db
from sqlalchemy import Column, Boolean, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func

import uuid

class TeacherOnAssignment(db.Model):
  __tablename__ = 'teacher_on_assignments'
  
  id = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
  is_active = Column(Boolean, default=True)
  created_at = Column(DateTime(timezone=True), default=func.now())
  updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=db.func.now())
  
  teacher_id = Column(UUID(as_uuid=True), nullable=False)
  assignment_id = Column(UUID(as_uuid=True), nullable=False)
  is_leader = Column(Boolean, default=False, nullable=False)
  __table_args__ = (
    UniqueConstraint('teacher_id', 'assignment_id', name='teacher_id_assignment_id'),
  )
  
  def __str__(self):
    s = [
      f'id = {self.id}',
      f'teacher_id = {self.teacher_id}',
      f'assignment_id = {self.assignment_id}'
    ]
    s = ', '.join(s)
    s = f'TeacherOnAssignment[{s}]'
    return s