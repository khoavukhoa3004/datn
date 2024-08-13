from flask import Response, jsonify
class BaseResponse:
  def __init__(self, data, message, status=200) -> None:
    self.data = jsonify({
        'data': data,
        'message': message
    })
    self.status = status

  def to_response(self):
    headers = {'Content-Type': 'application/json'}
    return self.data, self.status, headers

  @classmethod
  def of(cls, data):
      return BaseResponse(data, 'OK').to_response()

  @classmethod
  def error(cls, error):
      return BaseResponse('', error, 400).to_response()

  @classmethod
  def ok(cls):
      return BaseResponse('', 'OK').to_response()