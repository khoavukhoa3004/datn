from flaskr.database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import CheckConstraint
import uuid

class Assignment(db.Model):
  __tablename__ = 'assignments'
  
  id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
  name = db.Column(db.String, unique=True, nullable=False)
  description = db.Column(db.String, unique=False, nullable=True)
  
  def __str__(self):
    s = [
      f'id = {self.id}',
      f'name = {self.name}',
      f'description = {self.description}'
    ]
    s = ', '.join(s)
    s = f'Assignment[{s}]'
    return s