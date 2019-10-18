import toml, os, json, signal

from flask     import Flask, request
from abc       import ABC, abstractmethod
from time      import sleep
from threading import Thread

from components.pause import Pause
from components.board import Manager

class GameKilled(Exception):
  pass

class Game(ABC):
  """
  Provides a wrapper for game in/out interactions
  """

  def __init__(self, configpath):
    """
    Initalizes a new game wrapper

    :configpath <str> The path to the settings file
    """
    self._api = Flask(__name__)
    self._pause = Pause(self.pause_change)
    self._config = toml.load(configpath)
    self.manager = Manager(self.get_config('BOARD', 'STACK').split(','))
    self.meta = {}
    self.meta['time'] = {}
    self.meta['config'] = self._config
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
    """
    Gets an item from the config file

    :scope <str> the scope to look at
    :arg <str> the argument to get
    :default= <> a default value to be returned if an appropriate item cannot be found
    :type= <type> typecasts item to this type
    """
    default = kwargs.pop('default', None)
    _type = kwargs.pop('type', str)

    if default is not None and type(default) != _type:
      raise TypeError('default= must be %s' % type(_type))
    
    try:
      t = self._config[scope]
      return _type(t[arg])
    except KeyError as e:
      if default is None:
        raise e
      else:
        return _type(default)

  def kill(self, force=False):
    """
    Marks the game to safely quit

    :force <bool> force game to be killed immediatly
    """
    self._alive = False
    if force:
      self.killed()

  def killed(self):
    """
    If game has been marked "kill", actually kill the game
    """
    if self._alive == False:
      os.kill(os.getpid(), signal.SIGQUIT)

  def block(self):
    """
    To be used as a generic blocking method. Entering this method will test if the game is paused or has been killed
    """
    self.killed()
    self._pause.block_if_paused()

  def sleep(self, t=1):
    """
    Provides an interruptable sleep method

    :t <int> how long to sleep for
    """
    i = t
    while i > 0:
      self.block()
      i -= 1
      sleep(1)

  def _gameLoop(self, form):
    """
    The gameloop thread method
    """
    self.manager.resetall()
    self.gameLogic(form)
    self.kill(True)

  def _gameTimer(self):
    """
    The game timer thread method
    """
    # This will nuke threads too, thanks brad
    i = self._lifespan
    while i > 0 and self._playing:
      self.sleep()
      i -= 1
      self.game_tick(i)
      self.meta['time']['game_ticks'] = i
      if i == 0:
        self.kill(True)

  def _roundTimer(self):
    """
    The round timer thread method
    """
    i = self._roundtime
    while i > 0 and self._playing:
      self.round_tick(i)
      self.sleep()
      i -= 1
      self.meta['time']['round_ticks'] = i
    self.round_tick(-1)
    self._playing = False

  def startRound(self):
    """
    Starts a round
    """
    t = Thread(target=self._roundTimer)
    t.start()

  def stopRound(self):
    """
    Stop the round
    """
    self._playing = False

  def __call__(self, port=5000):
    """
    Alias for self.serve()
    """
    self.serve(port)

  def serve(self, port=5000):
    """
    Serves a set of http endpoints 

    :port <int=5000> what port to listen on
    """
    @self._api.route('/start', methods=['POST'])
    def flask_start_game():
      self._playing = True
      self._alive = True
      self.team = Team(request.form['team_name'], request.form['team_id'], request.form['team_playerCount'])
      self.meta['form'] = request.form.to_dict()
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
      try:
        return int(self.team)
      except AttributeError:
        return "Team doesn't exist because game hasn't started"

    @self._api.route('/dump')
    def flask_dump():
      return json.dumps(self.meta)

    @self._api.route('/kill')
    def flask_kill():
      self.kill()
      return 'killed'

    self._api.run(host='0.0.0.0', port=port)


class Team():

  def __init__(self, name, id, pc):
    self.name = name
    self.pc = int(pc)
    self.score = 0

  def __len__(self):
    return self.pc

  def __str__(self):
    return self.name

  def __int__(self):
    return self.score

  def __iadd__(self, o):
    self.score += o
    return self

  def __isub__(self, o):
    self.score -= o
    return self

