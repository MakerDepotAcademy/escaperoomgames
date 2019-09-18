from threading import Lock

class Pause():

  def __init__(self, hook):
    self._lock = Lock()
    self._hook = hook

  def block_if_paused(self):
    self._lock.acquire(True)
    self._lock.release()

  def isPaused(self):
    return self._lock.locked()

  def pause(self):
    if self.isPaused():
      self._lock.release()
      self._hook(False)
    else:
      self._hook(True)
      self._lock.acquire(True)