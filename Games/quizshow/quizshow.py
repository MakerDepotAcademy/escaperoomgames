#!/usr/bin/env python3
import sys, os
sys.path.append('./components')
from components.game import Game

from player import assignPlayers, cyclePlayers
import questions
from display import Display, displayQuestion

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
    ROUND_TIME = self.get_config('TIME', 'ROUND_TIME', type=int, default=10)
    self.disp.setRoundTimer(ROUND_TIME)
    self.disp.setGameTimer(self.get_config('TIME', 'GAME_TIME', type=int, default=300))
    
    self.disp.playVideo(self.get_config('VIDEOS', 'SPLASH', type=str))
    self.sleep(self.get_config('TIME', 'START_DELAY', type=int, default=1))

    plyrs = assignPlayers(len(self.team), self.manager)
    Q = questions.getQuestions(self.get_config('LINK', 'DB_URL'))
    P = cyclePlayers(plyrs)

    

    while True:
      # Match player to question
      question = next(Q)
      player = next(P)

      # Step 1: invite player
      self.block()
      # player.flash(Times.Invite_Sleep)
      player.lightAll(True)
      self.disp.invitePlayer(player._id)
      # self.disp.playAudio(START_MUSIC)
      # self.startRound()

      # Step 2: Display question
      self.block()
      question.show()
      displayQuestion(self.disp, question)

      # Step 3: Judge answer
      self.block()
      ans = player.catchAnswer(ROUND_TIME, self.round_tick)
      
      if ans is None:
        raise Exception('Answer cannot be none')

      if ans == '':
        self.disp.timeout()
        self.addScore(-1)
      else:
        if question == ans:
          self.disp.setCorrect(ans)
          self.addScore(1)
        else:
          self.disp.doWrong()
          self.disp.setSelected(ans)
          self.subScore(1)

      # Step 4 disinvite player
      self.disp.flush()
      player.lightAll(False)
      # self.stopRound()
      self.sleep(self.get_config('TIME', 'BETWEEN_ROUNDS', type=int, default=1))

QuizShowGame()()