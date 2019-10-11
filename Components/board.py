import serial
from pathlib import Path
from threading import Thread, Lock
import re
from random import randint
from time import sleep


class Board():
  """
  A driver for Brad's GPIO32 board
  """
  
  def __init__(self, port, qu=32, id=None):
    """
    Initalizes a driver

    :port <str> serial port to listen on
    :qu <int=32> how many pins are avaliable
    :id <any=None> vestigial, good for debugging
    """
    self._ser = serial.Serial(str(port), 2000000, timeout=1)
    self.flush()
    self._hooks = []
    self.queue = ['x'] * qu
    self._queuelen = qu
    self._id = id

  def close(self):
    """
    Closes the serial port
    """
    self._ser.close()

  def flush(self):
    """
    Flushes the serial port
    """
    self._ser.flushInput()
    self._ser.flushOutput()

  def run(self):
    """
    Runs the buffered commands
    """

    t = ''.join(self.queue) + '\n'
    self._ser.write(t.encode())
    self.queue = ['x'] * self._queuelen

  def reset(self):
    """
    Resets the board
    """

    def r(c):
      self.queue = c * 32
      self.run()
    r('U')
    r('I')
    r('0')

  def _setpin(self, pin, val):
    """
    Sets a pin to a value (buffred)
    """
    self.queue[pin] = val

  def _prompt(self, p):
    """
    Prompts the GPIO32 board by sending a command and returning the result

    :p <str> the data to send
    """
    self.run()
    self._ser.write(p.encode())
    r = self._ser.readline().decode()
    return r.strip()

  def turnOn(self, pin):
    """
    Turns on a pin

    :pin <int> the pin
    """
    self._setpin(pin, '1')

  def turnOff(self, pin):
    """
    Turns off pin

    :pin <int> the pin
    """
    self._setpin(pin, '0')

  def setInput(self, pin, inverse=False):
    """
    Sets a pin to input interrupt

    :pin <int> the pin
    :inverse <bool=False> if True sets pin to "pull down"
    """
    self._setpin(pin, 'u' if inverse else 'i')

  def unsetInput(self, pin, inverse=False):
    """
    Unsets a pin as input

    :pin <int> the pin
    :inverse <bool=False> if True sets pin to "pull down"
    """
    self._setpin(pin, 'U' if inverse else 'I')

  def setInterrupt(self, pin, enabled=True):
    """
    Sets pin to interrupt

    :pin <int> the pin
    :enabled <bool=True> sets the status of the pin
    """
    self._setpin(pin, 'e' if enabled else 'd')

  def getID(self):
    """
    Returns the id of the board
    """
    return self._prompt('?')
    
  def getLocation(self):
    """ 
    Gets the location
    """
    return self._prompt('l')
  
  def getPorts(self):
    """
    Gets the pin states
    """
    return self._prompt('r')

  def awaitChange(self, pins, timeout, timeout_tick=None):
    """
    Blocks until one of the pins mentioned is interrupted

    :pins <list(int)> the pins to detect
    :timeout <int> how long to wait
    :timeout_tick <callable> runs every second these pins aren't interrupted
    """
    def read(timeout=timeout):
      while timeout > 0:
        l = self._ser.readline()
        timeout -= 1
        timeout_tick(timeout)
        if re.match(r'[01]+', l.decode()):
          return l
      raise TimeoutError()
        
    buffer = read()

    while True:
      buffer += read()
      s = buffer.splitlines()
      new = s[-1]
      last = s[-2]
      if new != last:
        for p in pins:
          if new[p] != last[p]:
            del buffer
            return p
    

class Manager():
  """
  Manages multiple GPIO32 boards
  """
  
  def __init__(self, order):
    """
    Initalizes a new driver manager

    :order <list(int)> how to order the boards based on their ids
    """
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
    """
    Alias for self.getBoardByPos
    """
    return self.getBoardByPos(i)

  def __iter__(self):
    """
    Returns an iterator for the boards
    """
    return iter(self._boards)

  def getBoardByPos(self, i):
    """
    Get a board by it's position

    :i <int> the board id
    """
    return self._boards[i]

  def closeall(self):
    """
    Closes all drivers
    """
    for k in self._boards:
      self._boards[k].close()

  def resetall(self):
    """
    Resets all drivers
    """
    for k in self._boards:
      self._boards[k].reset()