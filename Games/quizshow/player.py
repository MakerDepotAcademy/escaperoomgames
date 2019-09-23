from time import sleep
from random import shuffle
from itertools import cycle

from questions import CHOICES
from components.board import Manager as M

class Button():

  def __init__(self, board, pin_out, pin_in):
    self._board = board
    self._in = pin_in
    self._out = pin_out

  def light(self, on=True):
    if on:
      self._board.turnOn(self._out)
    else:
      self._board.turnOff(self._out)

  def hook(self, h):
    self._board.onChange(h, self._in)

  def read(self):
    return self._board.readPin(self._in)

  def clearHooks(self):
    self._board.clearHooks()


class Player():
    
  def __init__(self, board, bot, id=None):
    self.buttons = {}
    tr = iter(range(bot, bot + 8))
    for c in CHOICES:
      self.buttons[c] = Button(board, next(tr), next(tr))
    self._board = board
    self._id = id

  def lightAll(self, on=True):
    for b in self.buttons:
      self.buttons[b].light(on)
    self._board.run()

  def flash(self, time):
    self.lightAll()
    sleep(time)
    self.lightAll(False)

  def __getitem__(self, x):
    return self.buttons[x]

  def catchAnswer(self, timeout=-1, timeout_tick=None):
    def b(i=None):
      if i != None:
        return self.buttons[CHOICES[i]]._in
      else:
        return [b(i) for i in range(len(CHOICES))]
        
    try:
      ret = self._board.awaitChange(b(), timeout, timeout_tick)
    except TimeoutError as e:
      return ''

    for i in range(3):
      if ret == b(i):
        return CHOICES[i]


def assignPlayers(player_count, boards):
  Players = []
  b = 0
  S = cycle(range(0, 32, 8))

  for i in range(player_count):
    b += len(Players) > Settings.Board_Player_Limit
    s = next(S)
    p = Player(boards[b], s, i + 1)
    Players.append(p)

  return Players

def cyclePlayers(players):
  # return cycle(players)
  while True:
    p = players
    shuffle(p)
    for i in p:
      yield i