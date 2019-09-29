import serial
from pathlib import Path
from threading import Thread, Lock
import re
from random import randint
from time import sleep


class Board():
  
  def __init__(self, port, qu=32, id=None):
    self._ser = serial.Serial(str(port), 2000000, timeout=1)
    self.flush()
    self._hooks = []
    self.queue = ['x'] * qu
    self._queuelen = qu
    self._id = id

  def close(self):
    self._ser.close()

  def flush(self):
    self._ser.flushInput()
    self._ser.flushOutput()

  def run(self):
    t = ''.join(self.queue) + '\n'
    self._ser.write(t.encode())
    self.queue = ['x'] * self._queuelen

  def reset(self):
    def r(c):
      self.queue = c * 32
      self.run()
    r('U')
    r('I')
    r('0')

  def _setpin(self, pin, val):
    self.queue[pin] = val

  def _prompt(self, p):
    self.run()
    self._ser.write(p.encode())
    r = self._ser.readline().decode()
    return r.strip()

  def turnOn(self, pin):
    self._setpin(pin, '1')

  def turnOff(self, pin):
    self._setpin(pin, '0')

  def setInput(self, pin, inverse=False):
    self._setpin(pin, 'u' if inverse else 'i')

  def unsetInput(self, pin, inverse=False):
    self._setpin(pin, 'U' if inverse else 'I')

  def setInterrupt(self, pin, enabled=True):
    self._setpin(pin, 'e' if enabled else 'd')

  def getID(self):
    return self._prompt('?')
    
  def getLocation(self):
    return self._prompt('l')
  
  def getPorts(self):
    return self._prompt('r')

  def awaitChange(self, pins, timeout, timeout_tick=None):
    def m(l):
      return re.match(r'[01]', l.decode())

    def readline(t=timeout):
      l = ''
      while t > 0:
        l = self._ser.readline()
        if l == b'':
          t -= 1
          if timeout_tick:
            timeout_tick(t)
        else:
          return l
      raise TimeoutError()
   
    for p in pins:
      self.setInput(p, True)
    self.run()

    print(pins)
    try:
      while True:
        readline(1)
    except TimeoutError:
      pass

    last = ''
    while not last:
      last = readline()
      last = '' if not m(last) else last
      
    while True:
      l = readline()
      if l == last:
        continue
      
      if m(l): 
        for p in pins:
          if l[p] != last[p]:
            return p

        last = l

class Manager():
  
  def __init__(self, order):
    self._boards = []
    t = {}
    
    for acm in Path('/dev').glob('ttyACM*'):
      b = Board(acm)
      for a in range(5): # For 5 attempts
        try:
          i = int(b.getID())
        except ValueError:
          continue
        else:
          t[i] = b
          print('Got board %s at %s' % (i, str(acm)))
          break

    for o in order:
      self._boards.append(t[int(o)])

  def __getitem__(self, i):
    return self.getBoardByID(i)

  def __iter__(self):
    return iter(self._boards)

  def getBoardByID(self, i):
    return self._boards[i]

  def closeall(self):
    for k in self._boards:
      self._boards[k].close()

  def resetall(self):
    for k in self._boards:
      self._boards[k].reset()