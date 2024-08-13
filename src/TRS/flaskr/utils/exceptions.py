from flask import jsonify
      
class CustomExceptionHandler:
  @staticmethod
  def handle_forbidden_resource(error):
    response = jsonify({'name': 'NO_RESOURCE', 'message': str(error)})
    response.status = 401
    return response, 401
  
  @staticmethod
  def handle_middlewares(error):
    response = jsonify({'name': '\033[92mERROR_MIDDLEWARES\033[0m','message': str(error)})
    response.status_code = 400
    return response

  @staticmethod
  def handle_bad_request_exception(error):
    response = jsonify({'name': 'BAD_REQUEST_EXCEPTION','message': str(error), 'statusCode': 400})
    # response.status_code = 400
    return response, 400, {'Content-Type': 'application/json', 'Status': 400, 'ETag': 'v1', 'Allow': '*'}

  @staticmethod
  def handle_not_found_exception(error):
    response = jsonify({'name': 'NOT_FOUND_EXCEPTION','message': str(error)})
    response.status_code = 404
    return response

  @staticmethod
  def handle_internal_server_exception(error):
    response = jsonify({'name': 'INTERNAL_SERVER_ERROR','message': str(error)})
    response.status_code = 500
    return response
  
class ForbiddenResourceException(Exception):
  pass 

class MiddlewareException(Exception):
  pass

class BadRequestException(Exception):
  pass

class NotFoundException(Exception):
  pass

class InternalServerException(Exception):
  pass