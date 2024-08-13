from datetime import datetime

def timeNow():
  time = datetime.now().strftime("%Y%m%d_%H%M%S")
  return time

def test():
  print(timeNow())
  
if __name__ == '__main__':
  test()