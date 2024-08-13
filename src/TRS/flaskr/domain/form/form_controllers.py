
from flask import Blueprint, request
from flaskr.utils.base_response import BaseResponse

from flaskr.domain.account.account_services import AccountService
from flaskr.domain.form.form_services import FormService

class FormController:
  form_controller = Blueprint('form_controller', __name__)
  
  @classmethod
  @form_controller.route('/api/forms', methods=['POST'])
  @AccountService.authenticate
  @AccountService.verify_student
  def create_form():
    '''
    Student need to fill out form first before getting new testcase sample.
    '''
    submission_id = request.json.get('submission_id')
    used_testcases = list(request.json.get('used_testcases'))
    ordered_testcases = list(request.json.get('ordered_testcases'))
    scores = request.json.get('scores')
    feedback = request.json.get('feedback')
    
    FormService.create(submission_id, ordered_testcases, used_testcases, scores, feedback)
    return BaseResponse.ok()
    

  

    