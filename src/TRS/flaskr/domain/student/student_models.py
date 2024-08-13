from flaskr.database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, func
from sqlalchemy.orm import relationship

from sqlalchemy.sql.sqltypes import DateTime
import uuid

class Student(db.Model):
  __tablename__ = 'students'
  
  id = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=db.func.now())
  account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id'), unique=True, nullable=False)
  account = relationship("Account", back_populates="student", uselist=False)
  mssv = Column(String, unique=True, nullable=True)
  assignments = relationship("Assignment", secondary='student_on_assignments', back_populates='students')
  submissions = relationship("Submission", backref='student', lazy=True)
  
  def __str__(self) -> str:
    s = [
      f'id = {self.id}',
    ]
    s = ', '.join(s)
    s = f'Student[{s}]'
    return s