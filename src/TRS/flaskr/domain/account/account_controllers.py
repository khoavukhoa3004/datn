from flask import Blueprint, request
from flaskr.utils.exceptions import BadRequestException
from flaskr.utils.base_response import BaseResponse
from flaskr.domain.account.account_services import AccountService
class AccountController:
  account_controller = Blueprint('account_controller', __name__)

  @classmethod
  @account_controller.route('/api/accounts/login/google', methods=['POST'])
  def login():
    token = request.json.get('token')
    account = AccountService.verify_token(token)
    print(account)
    return BaseResponse.of({
      'id': account.id,
      'name': account.name,
      'type': account.type.name,
      'email':account.email, 
    })

  @account_controller.route('/api/accounts', methods=['POST'])
  def create_account():
    secret = request.json.get('secret')
    if secret != 'sfscv3werqg':
      raise BadRequestException('PERMISSION_DENIED') 
    email = request.json.get('email')
    type = request.json.get('type')
    name = request.json.get('name')
    AccountService.create_account(name, email, type)
    return BaseResponse.ok()
    
  @classmethod
  @account_controller.route('/api/accounts', methods=['GET'])
  @AccountService.authenticate
  def get_account(cls):
    return AccountService.get_detail(account_id=request.account_id)
  

    
  
  