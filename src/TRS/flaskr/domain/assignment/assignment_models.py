from flaskr.database import db
from sqlalchemy import Column, Boolean, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func

import uuid

class Assignment(db.Model):
  __tablename__ = 'assignments'
  
  id = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
  name = Column(db.String, unique=True, nullable=False)
  is_active = Column(Boolean, default=True)
  created_at = Column(DateTime(timezone=True), default=func.now())
  updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=db.func.now())
  start_date = Column(DateTime(timezone=True))   # start time of assignment
  end_date = Column(DateTime(timezone=True))     # end time of assignment
  description = Column(db.String, nullable=True)
  
  author_id = Column(UUID(as_uuid=True), ForeignKey('teachers.id'), nullable=False)
  author = relationship("Teacher", foreign_keys=[author_id], back_populates='assignments')
  
  students = relationship("Student", secondary="student_on_assignments", back_populates='assignments')
  # collaborators = relationship("Teacher", secondary="teacher_on_assignments", back_populates='assignments')
  submission = relationship("Submission", back_populates='assignment', lazy=True)
  
  
  def __str__(self):
    s = [
      f'id = {self.id}',
      f'name = {self.name}',
      f'description = {self.description}'
    ]
    s = ', '.join(s)
    s = f'Assignment[{s}]'
    return s