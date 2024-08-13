
def success(data={}, message=''):
  return {
    'status': 'success',
    'data': data,
    'message': message
  }
  
def fail(data={}, message=''):
  return {
    'status': 'fail',
    'data': data,
    'message': message
  }