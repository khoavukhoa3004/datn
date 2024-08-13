from datetime import datetime
from flaskr.domain.account.account_models import Account
from flaskr.domain.account.account_services import AccountService
from flaskr.domain.assignment.assignment_teacher_models import TeacherOnAssignment
from flaskr.domain.teacher.teacher_models import Teacher
from flaskr.utils.exceptions import BadRequestException

from flaskr.domain.assignment.assignment_models import Assignment
from flaskr.domain.assignment.assignment_student_models import StudentOnAssignment
from flaskr.utils.base_response import BaseResponse
from flaskr.domain.student.student_models import Student
from sqlalchemy import or_, and_


class AssignmentService:
  @staticmethod
  def create(name: str, start_date: datetime, end_date: datetime, author_id: str, description):
    try: 
      a = Assignment(name=name, start_date=start_date, end_date=end_date, author_id=author_id, description=description)
      a.save()
    except:
      raise BadRequestException('INVALID_ERROR')
    
  @staticmethod
  def get_list(account: Account):
    if account.type.name == 'STUDENT':
      assignment_list = [
        dict(zip(['id', 'name', 'start_date', 'end_date', 'author_id', 'author_name'], row))
        for row in Assignment.query
        .join(StudentOnAssignment, StudentOnAssignment.assignment_id == Assignment.id)  # Join with StudentOnAssignment
        .join(Teacher, Assignment.author_id == Teacher.id)  # Separate join for Teacher
        .join(Account, Teacher.account_id == Account.id)
        .filter(StudentOnAssignment.student_id == account.student.id)
        .with_entities(
            Assignment.id,
            Assignment.name,
            Assignment.start_date,
            Assignment.end_date,
            Assignment.author_id,
            Account.name.label('author_name'),
        ).all()
]      
    else:
      assignments = Assignment.query.all()
      for item in assignments:
        teacher_on_assignment = TeacherOnAssignment.query.filter_by(assignment_id=item.id, teacher_id=item.author_id).first()
        if teacher_on_assignment == None:
          new_teacher_on_assignment = TeacherOnAssignment(teacher_id=item.author_id, assignment_id=item.id, is_leader=True)
          new_teacher_on_assignment.save()
      assignment_list = [
        dict(zip(['id', 'name', 'start_date', 'end_date', 'author_id', 'author_name'], row))
        for row in Assignment.query.with_entities(
        Assignment.id, 
        Assignment.name, 
        Assignment.start_date, 
        Assignment.end_date, 
        Assignment.author_id,
        )
        # .join(Teacher, Assignment.author_id == Teacher.id)
        # .join(Account, Teacher.account_id == Account.id)
        .filter(TeacherOnAssignment.teacher_id==account.teacher.id, TeacherOnAssignment.assignment_id==Assignment.id)
        .all()
      ]
    return assignment_list
    
  @staticmethod
  def allowed_file(filename):
    # Define the allowed file extensions
    allowed_extensions = {'xlsx', 'xls'}

    # Check if the file has an allowed extension
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in allowed_extensions
      
  @staticmethod
  def get_detail_student(id, account):
    if account.type.name == 'STUDENT':
      is_on_assignment = StudentOnAssignment.query.filter_by(assignment_id=id, student_id=account.student.id).first()
      if is_on_assignment == None:
        raise BadRequestException('PERMISSION_DENIED')
    else:
      is_on_assignment = TeacherOnAssignment.query.filter_by(assignment_id=id, teacher_id=account.teacher.id).first() != None or Assignment.query.filter_by(id=id, author_id=account.teacher.id).first() != None
      if not is_on_assignment:
        raise BadRequestException('PERMISSION_DENIED')
    assignment = Assignment.query.with_entities(
      Assignment.name,
      Assignment.start_date,
      Assignment.end_date,
      Assignment.author_id,
      Assignment.description
      ).filter_by(id=id).first()
    if not assignment:
      raise BadRequestException('ASSIGNMENT_NOT_FOUND')
    student_list = []
    teacher_list = []
    if account.type.name == 'TEACHER':
      student_list = [
        dict(zip(['id', 'mssv', 'name' ], row))
        for row in
        StudentOnAssignment.query
          .join(Student, Student.id == StudentOnAssignment.student_id)
          .join(Account, Account.id == Student.account_id)
          .filter(StudentOnAssignment.assignment_id == id, StudentOnAssignment.is_active == True)
          .with_entities(
            Student.id,
            Student.mssv,
            Account.name,
          ).order_by(Account.name.asc())
      ]
      teacher_list = [
        dict(zip(['id', 'name', 'is_leader', 'email'], row))
        for row in
        TeacherOnAssignment.query
          .join(Teacher, Teacher.id == TeacherOnAssignment.teacher_id)
          .join(Account, Account.id == Teacher.account_id)
          .filter(TeacherOnAssignment.assignment_id == id)
          .filter(TeacherOnAssignment.is_active == True)
          .with_entities(
            Teacher.id,
            Account.name,
            TeacherOnAssignment.is_leader,
            Account.email,
          ).order_by(Account.name.asc())
      ]
    author_name = Teacher.query.filter_by(id=assignment[3]).first()
    return {
      'name': assignment[0],
      'start_date': assignment[1],
      'end_date': assignment[2],
      'author_name': author_name.account.name,
      'description': assignment[4],
      'student_list': student_list,
      'teacher_list': teacher_list,
    } 
    
  @staticmethod
  def add_teacher_on_assignment(assignment_id: str, author_id: str, email: str, name: str):
    account = Account.query.filter_by(email=email).first()
    # If account student exist
    if account and account.type.name == 'STUDENT':
      raise BadRequestException('ACCOUNT_MUST_BE_TEACHER')
    
    # if account teacher exist. Check if teacher is already on assignment. If not, add teacher to assignment
    elif account and account.type.name == 'TEACHER':
      teacher = Teacher.query.filter_by(account_id=account.id).first()
      teacher_on_assignment = TeacherOnAssignment.query.filter_by(teacher_id=teacher.id, assignment_id=assignment_id).first()
      if teacher_on_assignment:
        raise BadRequestException('TEACHER_ALREADY_ON_ASSIGNMENT')
      if teacher:
        if author_id == teacher.id:
          new_teacher_on_assignment = TeacherOnAssignment(teacher_id=teacher.id, assignment_id=assignment_id, is_leader=True)
          new_teacher_on_assignment.save()
        else:
          new_teacher_on_assignment = TeacherOnAssignment(teacher_id=teacher.id, assignment_id=assignment_id)
          new_teacher_on_assignment.save()
    
    # if account is not found. Create new account and add to teacher on assignment
    else:
      _, teacher = AccountService.create_account(name=name, email=email, type='TEACHER', mssv=None)
      if teacher:
        teacher_on_assignment = TeacherOnAssignment(teacher_id=teacher.id, assignment_id=assignment_id)
        
