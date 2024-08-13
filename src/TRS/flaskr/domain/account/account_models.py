from flaskr.database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import Column, Boolean, Enum, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import enum
import uuid

class AccountTypeEnum(enum.Enum): 
	TEACHER = 'TEACHER'
	STUDENT = 'STUDENT'

class Account(db.Model):
  __tablename__ = 'accounts'
  
  id = Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
  email = Column(String, unique=True, nullable=False)
  password = Column(String, nullable=True)
  type = Column(Enum(AccountTypeEnum), nullable=False, default=AccountTypeEnum.STUDENT)
  is_active = Column(Boolean, default=True)
  created_at = Column(DateTime(timezone=True), default=func.now())
  updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=db.func.now())
  name = Column(String, nullable=False, default='')
  description = Column(String, unique=False, nullable=True)
  
  teacher = relationship("Teacher", back_populates="account", uselist=False)
  student = relationship("Student", back_populates="account", uselist=False)


  def __init__(self, name, email, type):
    super().__init__()
    self.name = name
    self.email = email
    self.type = type
    
  
  def __str__(self):
    s = [
      f'id = {self.id}',
      f'email = {self.email}',
			f'name = {self.email}',
      f'type = {self.type}',
			f'description = {self.password}'
		]
    s = ', '.join(s)
    s = f'Account[{s}]'
    return s