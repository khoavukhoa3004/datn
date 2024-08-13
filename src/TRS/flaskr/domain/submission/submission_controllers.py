from flask import Blueprint, request
from flaskr.domain.submission.submission_models import Submission
from flaskr.domain.assignment.assignment_student_models import StudentOnAssignment
from flaskr.utils.exceptions import BadRequestException
from flaskr.domain.account.account_services import AccountService
from flaskr.utils.base_response import BaseResponse


class SubmissionController:
  submission_controller = Blueprint('submission_controller', __name__)
  
  @classmethod
  @submission_controller.route('/api/submissions', methods=['GET'])
  @AccountService.authenticate
  @AccountService.verify_student
  def get_list():
    def handle_sumission(temp):
      item, index = temp[0], temp[1]
      if not item[3] or  len(item[3]) == 0:
        scores = 'Chương trình lỗi'
      else:
        current_scores = 100 * sum(score == True for score in item[3]) / len(item[3])
        if current_scores >= 90:
          scores = 'Rất tốt'
        elif current_scores < 90 and current_scores >=85:
          scores = 'Khá tốt'
        elif current_scores < 85 and current_scores >= 70:
          scores = "Khá"
        elif current_scores < 70:
          scores = 'Cần cải thiện'
        # print(f'score ne {sum(score == True for score in item[3])}, total: {len(item[3])}')
      return {
        'index': index,
        'id': item[0],
        'updated_at': item[1],
        'status': item[2].name,
        'scores': scores,
      }
    
    assignment_id = request.args.get('assignment_id')
    if not assignment_id:
      raise BadRequestException('INVALID_ASSIGNMENT_ID')
    student_on_assignment = StudentOnAssignment.query.filter_by(student_id=request.student.id,assignment_id=assignment_id)
    if not student_on_assignment:
      raise BadRequestException('ASSIGNMENT_NOT_FOUND')
    
    query = Submission.query \
      .filter_by(assignment_id=assignment_id, student_id=request.student.id) \
      .with_entities( 
        Submission.id, 
        Submission.updated_at, 
        Submission.status, 
        Submission.scores,
        ) \
      .order_by(Submission.updated_at.desc()) \
      .all()
    
    submissions = list(map(handle_sumission,zip(query, reversed(range(len(query))))))
    return BaseResponse.of(submissions)