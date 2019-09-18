import toml

with open('./config.cfg') as c:
  _config = toml.loads(c.read())


class Section():

  def __init__(self, name):
    self._section = _config[name]

  def show(self):
    print(self._section)

  def _get(self, key, default=None):
    try:
      return self._section[key]
    except KeyError as e:
      if default is None:
        raise e
      else:
        return default

  def _getint(self, key, default=None):
    return int(self._get(key, default))


class Time(Section):

  def __init__(self):
    Section.__init__(self, 'TIME')
    self.Game_Time = self._getint('GAME_TIME')
    self.Round_Time = self._getint('ROUND_TIME')
    self.Invite_Sleep = self._getint('INVITE_SLEEP', 1)
    self.StartDelay = self._getint('START_DELAY')
    self.AmbientDelay = self._getint('AMBIENT_DELAY')
    self.WarningTime = self._getint('WARNING_TIME', 15)


class BoardStack(Section):

  def __init__(self):
    Section.__init__(self, 'BOARDS')
    self.Board_Stack = [int(i) for i in self._get('BOARD_STACK').split(',')]
    self.Board_Player_Limit = self._get('BOARD_PLAYER_LIMIT', 4)


class Scores(Section):

  def __init__(self):
    Section.__init__(self, 'SCORES')
    self.Inc = self._getint('INC', 1)
    self.Dec = self._getint('DEC', 1)
    self.Init_Score = self._getint('INIT', 0)


class Database(Section):

  def __init__(self):
    Section.__init__(self, 'DATABASE')
    self.URL = self._get('URL')


class Links(Section):

  def __init__(self):
    Section.__init__(self, 'LINKS')
    self.Display_Host = self._get('DISP')
    self.Me = self._get('ME', 'localhost:5000')

class Music(Section):

  def __init__(self):
    Section.__init__(self, 'MUSIC')
    self.Start = self._get('START')
    self.Ambient = self._get('AMBIENT')
    self.Warning = self._get('WARNING')
    self.Correct = self._get('CORRECT')
    self.End = self._get('END')
    self.Wrong = self._get('WRONG')