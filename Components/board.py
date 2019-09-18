import serial
from pathlib import Path
from threading import Thread, Lock
import re
from random import randint
from time import sleep
import components.settings as Settings

DEV = False
DEV_COUNT = 2
DEV_BIDS = iter(Settings.BoardStack().Board_Stack)

class DevSerial():
  
  def __init__(self, port, baudrate=2000000, timeout=1):
    self._port = port
    self._br = baudrate
    self._timeout = timeout
    self._status = ['x'] * 32
    self._pins = ['0'] * 32
    self._read_stack = []
    self._id = next(DEV_BIDS)
    self.closed = False

  def write(self, d):
    if self.closed:
      raise Exception('Serial is closed')

    d = [chr(i) for i in d]
    if len(d) >= 32:
      for i in range(32):
        if d[i] != 'x':
          self._status[i] = d[i]
      return

    if d[0] == '?':
      self._read_stack.append(self._id)
      return

    if d[0] == 'l':
      return

    if d[0] == 'v':
      self._read_stack.append('dev')

    if d[0] == 'r':
      self._read_stack.append(self._pins)
      return

    if d[0] == 'R':
      self._read_stack.append(self._status)
      return

    if d[0] == 's':
      self._status[d[1:-1]] = d[-1]
      return

  def readline(self):
    if self._read_stack == []:
      sleep(self._timeout)
      return ''
    else:
      return str(self._read_stack.pop()).encode()

  def close(self):
    self.close = True

  def flushInput(self):
    pass

  def flushOutput(self):
    pass

  def interrupt(self, pin, val=-1):
    buff = self._status
    buff[pin] = not buff[pin] if val == -1 else val
    self._read_stack.append(buff)


class Board():
  
  def __init__(self, port, qu=32, id=None):
    if DEV:
      self._ser = DevSerial(port)
    else:
      self._ser = serial.Serial(str(port), 2000000, timeout=1)
    self.flush()
    self._hooks = []
    self.queue = ['x'] * qu
    self._queuelen = qu
    self._eventThread = Thread(target=self._eventLoop)
    self._eventAlive = False
    self._eventLock = Lock()
    self._id = id

  def close(self):
    self._ser.close()

  def flush(self):
    self._ser.flushInput()
    self._ser.flushOutput()

  def _eventLoop(self):
    last = ''
    while True:
      self._eventLock.acquire(True)
      line = self._ser.readline()
      self._eventLock.release()

      if len(line) == 0 or last == line:
        continue
      
      for i, (c, l) in enumerate(zip(line, last)):
        if c != l:
          for hook, pin in self._hooks:
            if pin == -1 or pin == i + 1:
              hook(pin, c == '1')

      last = line

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
    self._eventLock.acquire(True)
    self._ser.write(p.encode())
    r = self._ser.readline().decode()
    self._eventLock.release()
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

  def onChange(self, hook, pin=-1):
    self._hooks.append((hook, pin))
    
    if pin == -1:
      self.queue = 'e' * self._queuelen
    else:
      self.queue[pin - 1] = 'e'

    self.run()

    if not self._eventAlive:
      self._eventThread.start()
      self._eventAlive = True

  def clearHooks(self):
    self._hooks = []
    self.queue = 'd' * self._queuelen
    self.run()

  def clearHook(self, pin):
    for i, ent in enumerate(self._hooks):
      if ent[1] == pin:
        del self._hooks[i]
        self.queue[pin - 1] == 'd'

    self.run()

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
  
  def __init__(self):
    self._boards = {}
    l = None
    if DEV:
      l = range(len(Settings.BoardStack().Board_Stack))
    else:
      l = Path('/dev').glob('ttyACM*')
    
    for acm in l:
      b = Board(acm)
      for a in range(5): # For 5 attempts
        i = b.getID()
        if re.search(r'[0-9]+', i):
          self._boards[int(i)] = b
          print('Got board %s at %s' % (i, str(acm)))
          break
  

  def __getitem__(self, i):
    return self.getBoardByID(i)

  def __iter__(self):
    return iter(self._boards)

  def getBoardByID(self, i):
    return self._boards[i]

  def closeall(self):
    for k in self._boards:
      self._boards[k].close()