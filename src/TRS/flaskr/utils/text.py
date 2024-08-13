import string
import random

def random1character():
  return random.choice(string.ascii_letters)

def encrypt(s: str):
  '''
  simpleencrypt
  '''
  # TODO: nhớ dùng khi gửi id của Recommendation
  s = str(s)
  l = len(s)
  n = l // 2
  
  s = s[n:] + s[:n]
  s = random1character() + s + 'U'
  return s
  
def decrypt(s: str):
  '''
  simpledecrypt
  '''
  s = s[1:-1]
  l = len(s)
  n = l // 2
  
  s = s[n:] + s[:n]
  return s


def genLinkBy(id):
  enid = encrypt(id)
  return enid
  
def testGenLinkBy():
  id = '04a68414-094f-4d19-b757-646fbfbfec11'
  encrypt_id = genLinkBy(id)
  link = f'https://coderunner.codepractice.net/api/testcases/{encrypt_id}'
  print(link)

if __name__ == '__main__':
  testGenLinkBy()