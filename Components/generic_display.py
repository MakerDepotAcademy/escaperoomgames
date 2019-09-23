from json import dumps
import websocket

class Display():
  
  def __init__(self, address, **kwargs):
    self._address = address
    self._payload = dict()
    self.isPaused = False
    self.isRunning = False
    self._ws = websocket.WebSocket()
    self._ws.connect('ws://' + self._address)

  def _queue(self, endpoint, payload=None):
    if endpoint in self._payload.keys():
      self.flush()
    self._payload[endpoint] = payload

  def flush(self):
    print(self._payload)
    self._ws.send(dumps(self._payload))
    self._payload = dict()

  def setRoundTime(self, t):
    self._queue('round_time', t)

  def setGameTime(self, t):
    self._queue('game_time', t)

  def setScore(self, s):
    self._queue('score', s)
