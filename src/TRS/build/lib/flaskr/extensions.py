from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.ext.declarative import declared_attr
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func
import uuid
from flask import current_app

class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @declared_attr
    def id(cls):
        return sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    @declared_attr
    def created_at(cls):
        return sa.Column(DateTime(timezone=True), default=func.now())

    @declared_attr
    def updated_at(cls):
        return sa.Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    @declared_attr
    def deleted_at(cls):
        return sa.Column(DateTime(timezone=True), default=None)

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        print("save the record")
        print(self)
        print("End_____________________")
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
                return True
            except Exception as e:
                current_app.logger.error('Error when save file:', e)
                db.session.rollback()
                raise DBCommitException(e)
                
        return self

    def delete(self, hard_delete=False, commit=True):
        """Remove the record from the database."""
        if hard_delete:
            db.session.delete(self)
            if commit:
                try:
                    db.session.commit()
                    return True
                except Exception as e:
                    current_app.logger.error('Error when delete file:', e)
                    db.session.rollback()
                    raise DBCommitException(e)

            return False
        else:
            return self.deleted_at is None and self.update(commit, deleted_at=func.now())

class DBCommitException(Exception):
    def __init__(self, msg) -> None:
        self.msg = f'Error in Commit: {msg}'
        super().__init__(self.msg)
    
    def __str__(self) -> str:
        return self.msg
    
db = SQLAlchemy(model_class=CRUDMixin)