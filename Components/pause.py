from threading import Lock

class Pause():
  """
  A semaphore for pausing the game
  """

  def __init__(self, hook=None):
    """
    Initalizes a semaphore

    :hook <callable> runs when the semaphore is changed
    """
    self._lock = Lock()
    self._hook = hook

  def block_if_paused(self):
    """
    Blocks process if semaphore is locked
    """
    self._lock.acquire(True)
    self._lock.release()

  def isPaused(self):
    """
    Returns if the semaphore is locked
    """
    return self._lock.locked()

  def pause(self):
    """
    Toggles the semaphore
    """
    if self.isPaused():
      self._lock.release()
      self._hook(False)
    else:
      self._hook(True)
      self._lock.acquire(True)