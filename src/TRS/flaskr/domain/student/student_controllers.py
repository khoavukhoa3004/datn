


from flask import Blueprint, request

from flaskr.domain.account.account_services import AccountService
from flaskr.domain.student.student_services import StudentService


class StudentController:
  student_controller = Blueprint('student_controller', __name__)
  
  @classmethod
  @student_controller.route('/api/students', methods=['POST',])
  @AccountService.authenticate
  @AccountService.verify_teacher
  def update_student_list():
    StudentService.update_student_list(request.files)
    return 'Upload successfully'