import unittest
import lib

def forAllBoards(fn):
  def wrapper(self):
    for id in self.manager:
      self.thisBoard = self.manager[id]
      fn(self)

  return wrapper

def forAllPins(fn):
  def wrapper(self):
    for i in range(self.thisBoard._queuelen):
      self.thisPin = i
      fn(self)
    self.thisBoard.run()
    self.thisBoard.reset()
    self.assertTrue(True)

  return wrapper

class Lib_Test(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.manager = lib.Manager()

  @classmethod
  def tearDownClass(cls):
    cls.manager.closeall()

  @forAllBoards
  @forAllPins
  def test_turnAllOn(self):
    self.thisBoard.turnOn(self.thisPin)

  @forAllBoards
  @forAllPins
  def test_turnAllOff(self):
    self.thisBoard.turnOff(self.thisPin)

  @forAllBoards
  @forAllPins
  def test_setAllInputs(self):
    self.thisBoard.setInput(self.thisPin)

  @forAllBoards
  @forAllPins
  def test_setAllInputsPullup(self):
    self.thisBoard.setInput(self.thisPin, True)

  @forAllBoards
  def test_getLocation(self):
      l = self.thisBoard.getLocation()
      self.assertTrue(l)

  @forAllBoards
  def test_getPorts(self):
      l = self.thisBoard.getPorts()
      self.assertTrue(l)

  @forAllBoards
  def test_getIDs(self):
      l = self.thisBoard.getID()
      self.assertTrue(l)

  @forAllBoards
  @forAllPins
  def test_awaitChange(self):
    print('Please press ' + str(self.thisPin))
    r = self.thisBoard.awaitChange([self.thisPin], 100)
    self.assertEqual(r, self.thisPin)


if __name__ == '__main__':
  unittest.main()