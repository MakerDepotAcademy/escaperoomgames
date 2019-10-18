#!/usr/bin/env python3
import sys, os
sys.path.append('./components')
from components.game import Game

from player import assignPlayers, cyclePlayers, NoAnswer
import questions
from display import Display, displayQuestion

import logging

FORMAT = '%(asctime)-15s %(name)s : %(message)s'
logging.basicConfig(filename='qs.log',format=FORMAT,level=logging.NOTSET)

logger = logging.getLogger(__name__)


class QuizShowGame(Game):

  def __init__(self):
    Game.__init__(self, os.getcwd() + '/config.cfg')
    self.disp = Display(self.get_config('LINK','DISP'), correct_music=self.get_config('MUSIC', 'START'), wrong_music=self.get_config('MUSIC', 'WRONG'))
    self.disp.restart()
    self.meta['score'] = {}
    self.meta['score']['correct'] = 0
    self.meta['score']['wrong'] = 0

  def game_tick(self, time):
    self.disp.setGameTimer(time)

  def round_tick(self, time):
    self.disp.setRoundTimer(time)

  def once_killed():
    self.disp.restart()

  def pause_change(paused):
    print('Pause')
    print(paused)

  def _set_score(self):
    self.disp.setScore(int(self.team))

  def addScore(self, s):
    self.meta['score']['correct'] += s
    self.team += s
    self._set_score()

  def subScore(self, s):
    self.meta['score']['wrong'] += s
    self.team -= s
    self._set_score()

  def gameLogic(self, form):
    # Pregame prep
    self.disp.restart()
    ROUND_TIME = self.get_config('TIME', 'ROUND_TIME', type=int, default=10)
    self.disp.setRoundTimer(ROUND_TIME)
    self.disp.setGameTimer(self.get_config('TIME', 'GAME_TIME', type=int, default=300))
    
    self.disp.playVideo(self.get_config('VIDEOS', 'SPLASH', type=str))
    self.sleep(self.get_config('TIME', 'START_DELAY', type=int, default=1))

    plyrs = assignPlayers(len(self.team), self.manager)
    Q = questions.getQuestions(self.get_config('LINK', 'DB_URL'))
    P = cyclePlayers(plyrs)

    for b in self.manager:
      for i in range(32):
        b.turnOff(i)
      b.run()

    while True:
      # Match player to question
      question = next(Q)
      logger.debug("Got question")
      player = next(P)
      logger.debug("Got player")

      # Step 1: invite player
      self.block()
      logger.debug("Invite player")
      # player.flash(Times.Invite_Sleep)
      player.lightAll(True)
      logger.debug("Light player podium")
      self.disp.invitePlayer(player._id)
      logger.debug("Invite player flash")
      # self.disp.playAudio(START_MUSIC)
      # self.startRound()

      # Step 2: Display question
      self.block()
      logger.debug("Loading question")
      question.show()
      displayQuestion(self.disp, question)
      logger.debug("Posted question to display")

      # Step 3: Judge answer
      self.block()
      logger.debug("Judging answer")
      ans = player.catchAnswer(ROUND_TIME, self.round_tick)
      logger.debug("Caught answer %s" % ans)
      
      if ans is None:
        logger.debug("Answer is none")
        raise Exception('Answer cannot be none')

      if ans == '':
        self.disp.timeout()
        logger.debug("Display timeout flash")
        self.subScore(1)
        logger.debug("Sub 1 from score")
      else:
        if question == ans:
          logger.debug("Correct answer")
          self.disp.setCorrect(ans)
          logger.debug("Correct answer flash")
          self.addScore(1)
          logger.debug("Add score")
        else:
          self.disp.doWrong()
          logger.debug("Wrong answer flash")
          self.disp.setSelected(ans)
          logger.debug("Set %a to selected" % ans)
          self.subScore(1)
          logger.debug("Sub one from score")

      # Step 4 disinvite player
      logger.debug("Disinvite player")
      self.disp.flush()
      logger.debug("Clear display buffer")
      player.lightAll(False)
      logger.debug("Turn off podium")
      # self.stopRound()
      self.sleep(self.get_config('TIME', 'BETWEEN_ROUNDS', type=int, default=1))

QuizShowGame()()