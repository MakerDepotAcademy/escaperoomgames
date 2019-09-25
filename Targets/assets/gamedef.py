#!/usr/bin/env python3
import sys, os
sys.path.append('./components')
from components.game import Game

# Welcome to your new game
# From here, you need to define all of {{name}}'s behaviors. Every method you 
# see here has to be implemented.

class {{name}}(Game):

  def __init__(self):
    Game.__init__('config.cfg')
    # Use this space here to initalized any display drivers or other assets

  # Use this space to define any other methods the game needs

  def gameLogic(self, form):
    # This is the method that runs the game, after it returns the game will be
    # killed. `form` is a dictionary of all key=value pairs delivered in the 
    # request form
    pass

  def pause_change(self, paused):
    # This method gets triggered whenever the game hase been paused/unpaused
    pass

  def game_tick(self, time):
    # This happens everytime the internal game timer changes
    pass

  def round_tick(self, time):
    # This happens everytime the round timer changes
    pass

  def once_killed(self):
    # This happens right before the game is officially killed. Use this to reset
    # any external assets.
    pass

{{name}}()()