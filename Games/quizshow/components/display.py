from json import dumps
from components.questions import CHOICES
from components.settings import Music
import websocket

M = Music()

class DONOTUSEME(Exception):

    def __init__(self):
        Exception.__init__("Do Not Use Me")

class Display():

    def __init__(self, address):
        self._address = address
        self._payload = dict()
        self.isPaused = False
        self.isRunning = False
        self._ws = websocket.WebSocket()
        self._ws.connect('ws://' + self._address)

    def _queue(self, endpoint, payload=None):
        self._payload[endpoint] = payload

    def flush(self):
        print(self._payload)
        self._ws.send(dumps(self._payload))
        self._payload = dict()

    def setQuestion(self, question):
        self._queue('question', question)

    def _getLabel(self, label, edge=None):
        edge = '.' + edge if edge is not None else ''
        return label + edge

    def setAnswer(self, label, answer):
        self._queue(self._getLabel(label), answer)

    def setCorrect(self, label):
        self._queue(self._getLabel('score', 'correct'))
        self._queue(self._getLabel(label, 'correct'))
        self.playAudio(M.Correct)

    def setSelected(self, label):
        self._queue(self._getLabel(label, 'selected'))

    def setScore(self, score):
        pass

    def setRoundTimer(self, secs):
        self._queue('roundtick', secs)
        self.flush()
    
    def setGameTimer(self, secs):
        self._queue('gametick', secs)
        self.flush()

    def doWrong(self):
        self._queue(self._getLabel('score', 'wrong'))
        self._queue('wrong')
        self.playAudio(M.Wrong)

    def playVideo(self, vidpath):
        self._queue('videoplay', vidpath)
        self.flush()

    def playAudio(self, audpath):
        self._queue('audioplay', audpath)
        self.flush()

    def restart(self):
        self._queue('restart')
        self.flush()
        
    def invitePlayer(self, label):
        self._queue('player', label)
        self.flush()

    def timeout(self):
        self._queue('timeout')
    

def displayQuestion(display, question):
    display.setQuestion(question.question)
    for c in CHOICES:
        display.setAnswer(c, question.answers[c])

    display.flush()