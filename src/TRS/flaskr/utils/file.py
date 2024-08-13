from constants import FILE_WITH_ID,FILE_SUBMISSION_PATH
from flaskr.utils.time import timeNow

class File:
  
  def getStudentId(filepath):
    '''
    return None if can't detect student's id
    '''
    # TODO: implement
    with open(filepath, 'r', errors='ignore') as f:
      line = f.readline() # contains '\n' at the end
      if line[-1] == '\n':
        line = line[:-1]

      if len(line) > 20:
        return None
      if len(line) < 3:
        return None
      
      return line[3:]
    
  def checkStudentId(id):
    # simple check
    if len(id) > 20 or len(id) < 3:
      return False
    return True
  
  def save():
    pass
  
def readall(filepath):
  with open(filepath, 'r') as f:
    return f.read()
  
def testReadall():
  return readall('')