from flaskr.database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.orm import relationship

from sqlalchemy.sql.sqltypes import DateTime
import uuid

class Teacher(db.Model):
  __tablename__ = 'teachers'
  
  id = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=db.func.now())

  account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id'), unique=True, nullable=False)
  account = relationship("Account", back_populates="teacher", uselist=False)
  # collaborators = relationship("Assignment", secondary="teacher_on_assignments", back_populates='teachers')
  # assignments = relationship("Assignment", backref='author', lazy=True)
  
  assignments = relationship("Assignment", back_populates='author', lazy=True)