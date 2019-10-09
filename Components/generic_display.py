from json import dumps
import websocket

class Display():
  """
  A driver for the generic display
  """
  
  def __init__(self, address):
    """
    Initalizes a new display driver

    :address <str> the address to the display
    """
    self._address = address
    self._payload = dict()
    self.isPaused = False
    self.isRunning = False
    self._ws = websocket.WebSocket()
    self._ws.connect('ws://' + self._address)

  def _queue(self, endpoint, payload=None):
    """
    Queues a command to send to the display

    :endpoint <str> the command to send
    :payload <any> the arguments to send
    """

    if endpoint in self._payload.keys():
      self.flush()
    self._payload[endpoint] = payload

  def flush(self):
    """
    Sends the payload
    """
    print(self._payload)
    self._ws.send(dumps(self._payload))
    self._payload = dict()

  def setRoundTime(self, t):
    """
    Sets the round timer

    :t <int> the number to display
    """
    self._queue('round_time', t)

  def setGameTime(self, t):
    """
    Sets the game timer

    :t <int> the number to display
    """
    self._queue('game_time', t)

  def setScore(self, s):
    """
    Sets the score

    :t <int> the number to display
    """
    self._queue('score', s)

  def timeout(self):
    """
    Flashes the "round's up" message
    """
    self._queue('roundsup')

  def good(self):
    """
    Flashes the "good" message
    """
    self._queue('correct')

  def gameover(self):
    """
    Flashes the "game over" message
    """
    self._queue('gameover')