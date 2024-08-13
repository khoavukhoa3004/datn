import threading
from constants import MAX_NO_THREADS

threadLimiter = threading.BoundedSemaphore(5)

class LimitThread(threading.Thread):
  def run(self):
    threadLimiter.acquire()
    try:
      super().run()
    finally:
      threadLimiter.release()