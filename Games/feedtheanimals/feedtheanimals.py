#!/usr/bin/env python3
import sys, os
sys.path.append('./components')
from components.game import Game
from hole import HoleManager

class Feed_The_Animals(Game):

  def __init__(self):
    Game.__init__(os.getcwd() + '/config.cfg')

  def gameLogic(form):
    M = HoleManager(self.manager)
    while True:
      M.select(self.get_config('GAME', 'HOLE_COUNT', type=int, default=5))
      M.awaitAllTriggered(self.get_config('TIME', 'ROUND_TIME', type=int, default=20))
      # TODO: Push to display