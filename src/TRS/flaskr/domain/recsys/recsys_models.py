from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from flaskr.database import db

class Recommendation(db.Model):
  __tablename__ = 'recommendation'
  
  # id
  
  # status
  # 1: mới insert, chua tinh toan -> nếu có request tới thì thông báo chờ
  # 2: đã hết testcases để gợi ý (số lượng tc còn lại < 5)
  # 3: gợi ý thành công - list_testcase_id sẽ khác rỗng
  # 4: chưa làm đúng tất cả các testcase của lần gợi ý trước
  # 5: đã đạt số lần gợi ý tối đa trong 1 ngày (5)
  status = db.Column(db.Integer, unique=False, nullable=False)

  # this recommendation is after this submission_id
  submission_id = db.Column(UUID(as_uuid=True), ForeignKey('submissions.id'), unique=True, nullable=False)
  submission = relationship("Submission", foreign_keys=[submission_id], back_populates="recommendation", uselist=False)

  list_testcase_id = db.Column(ARRAY(db.Integer), unique=False, nullable=False)
  list_false_tcids = db.Column(ARRAY(db.Integer), unique=False, nullable=True)
  
  # level: 1-de, 2-TB, 3-kho
  # độ khó tương ứng với performance hiện tại của sinh viên
  level = db.Column(db.Integer, unique=False, nullable=True)
  # url
  # Lần 1 insert: chuỗi rỗng ''
  # lần 2 update
  # url = db.Column(db.String, unique=True, nullable=False, default='')
  is_filled_form = db.Column(db.Boolean, nullable=False, default=False)
  
  def __str__(self) -> str:
    s = [
      f'status = {self.status}',
      f'submission_id = {self.submission_id}',
      f'list_testcase_id = {self.list_testcase_id}',
      f'level = {self.level}'
    ]
    s = ', '.join(s)
    s = f'Recommendation[{s}]'
    return s