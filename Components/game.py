import toml

from flask import Flask, request
from abc import ABC, abstractmethod
from time import sleep
from threading import Thread

from components.pause import Pause
from components.board import Manager

class GameKilled(Exception):
  pass

class Game(ABC):

  def __init__(self, configpath):
    self._api = Flask(__name__)
    self._pause = Pause(self.pause_change)
    self._config = toml.load(configpath)
    self.manager = Manager(self.get_config('BOARD', 'STACK').split(','))
    self.meta = {}
    self._alive = True
    self._lifespan = self.get_config('TIME', 'GAME_TIME', type=int, default=300)
    self._playing = False
    self._roundtime = self.get_config('TIME', 'ROUND_TIME', type=int, default=10)

  @abstractmethod
  def gameLogic(self, form):
    pass

  @abstractmethod
  def pause_change(self, paused):
    pass

  @abstractmethod
  def game_tick(self, time):
    pass

  @abstractmethod
  def round_tick(self, time):
    pass

  @abstractmethod
  def once_killed(self):
    pass

  def get_config(self, scope, arg, **kwargs):
    default = kwargs.pop('default', None)
    _type = kwargs.pop('type', str)

    if default is not None and type(default) != _type:
      raise TypeError('default= must be %s' % type(_type))
    
    t = self._config[scope]
    try:
      return _type(t[arg])
    except KeyError as e:
      if default is None:
        raise e
      else:
        return _type(default)

  def kill(self, force=False):
    self._alive = False
    if force:
      self.killed()

  def killed(self):
    if self._alive == False:
      for b in self.manager:
        b.resetall()
        b.closeall()
      self.once_killed()
      raise GameKilled('Game has been killed')

  def block(self):
    self.killed()
    self._pause.block_if_paused()

  def sleep(self, t=1):
    i = t
    while i > 0:
      self.block()
      i -= 1
      sleep(1)

  def _gameLoop(self):
    self.gameLogic()
    self.kill(True)

  def _gameTimer(self):
    # This will nuke threads too, thanks brad
    i = self._lifespan
    while i > 0 and self._playing:
      self.sleep()
      i -= 1
      self.game_tick(i)
      if i == 0:
        # Kill game
        self.kill(True)

  def _roundTimer(self):
    i = self._roundtime
    while i > 0 and self._playing:
      self.round_tick(i)
      self.sleep()
      i -= 1
    self.round_tick(-1)
    self._playing = False
      

  def startRound(self):
    t = Thread(target=self._roundTimer)
    t.start()

  def stopRound(self):
    self._playing = False

  def serve(self, port=5000):
    @self._api.route('/start', methods=['POST'])
    def flask_start_game():
      self._playing = True
      self._alive = True
      self._gameloopthread = Thread(target=self._gameLoop, args=[request.form.to_dict()])
      self._gametimerthread = Thread(target=self._gameTimer)
      self._gameloopthread.start()
      self._gametimerthread.start()

      return 'started'

    @self._api.route('/pause')
    def flask_pause_game():
      self._pause.pause()
      if self._pause.isPaused():
        return 'Game is paused'
      else:
        return 'Game is running'

    @self._api.route('/score')
    def flask_get_score():
      return str(Scores.score)

    @self._api.route('/dump')
    def flask_dump():
      return self.meta

    @self._api.route('/kill')
    def flask_kill():
      self.kill()
      return 'killed'

    self._api.run(host='0.0.0.0', port=port)
