from random import sample
from time import time

class StopWatch():

  def __init__(self):
    self._s = 0
    self._e = 0

  def start(self):
    self._s = time()

  def stop(self):
    self._e = time()
    self.time = self._e = self._s

  def __enter__(self):
    self.start()

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.stop()

  def __int__(self):
    return self.time

class HoleManager():
  
  def __init__(self, board):
    self._b = board
    self._holes = []
    self._chosen = []

    r = range(self._b.queuelen)
    while True:
      try:
        self._holes.append(Hole(board, next(r), next(r)))
      except StopIteration:
        break

  def flush(self):
    self._b.flush()

  def select(self, count=5):
    self._chosen = sample(self._holes, count)
    for i in self._chosen:
      c.turnOn()

    self.flush()

  def awaitAllTriggered(self, timeout, timeout_tick):
    ins = list(self._chosen)
    S = StopWatch()
    T = timeout
    while len(ins) > 0:
      S.start()
      p = self._b.awaitChange([i._in for i in ins], T, timeout_tick)
      S.stop()
      T -= int(S)
      ins.remove([i for i in ins if i._in == p][0])

    return True


class Hole():

  def __init__(self, board, i, o):
    self._b = board
    self._in = i
    self._out = o

  def turnOn(self):
    self._b.turnOn(self._out)

  def turnOff(self):
    self._b.turnOff(self._out)

  def flush(self):
    self._b.flush()
