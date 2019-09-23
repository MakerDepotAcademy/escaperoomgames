#!/usr/bin/env python3
import sys, os
sys.path.append('./components')
from components.game import Game
from components.generic_display import Display
from hole import HoleManager

disp = None

class Feed_The_Animals(Game):

  def __init__(self):
    Game.__init__(os.getcwd() + '/config.cfg')
    disp = Display(self.get_config('LINKS', 'DISP'))

  def game_tick(self, t):
    disp.setGameTime(t)
    disp.flush()

  def round_tick(self, t):
    disp.setRoundTime(t)
    disp.flush()

  def pause_change(self, paused):
    pass

  def once_killed(self):
    pass

  def gameLogic(form):
    M = HoleManager(self.manager)
    score = 0
    dscore = self.get_config('GAME', 'HOLE_COUNT', type=int, default=5)
    while True:
      M.select(dscore)
      res = M.awaitAllTriggered(self.get_config('TIME', 'ROUND_TIME', type=int, default=20), self.round_tick)
      if res:
        disp.good()
      else:
        disp.timeout()
      score += dscore * (1 if res else -1)
      disp.setScore(score)
      disp.flush()