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

  def game_tick(self, time):
    self.disp.setGameTimer(time)

  def round_tick(self, time):
    self.disp.setRoundTimer(time)

  def once_killed():
    print('Killed')

  def pause_change(paused):
    print('Pause')
    print(paused)

  def addScore(self, s=None):
    if s is not None:
      self.meta['score'] += s
    return self.meta['score']

  def gameLogic(self, form):
    # Pregame prep
    ROUND_TIME = self.get_config('TIME', 'ROUND_TIME', type=int, default=10)
    self.disp.setRoundTimer(ROUND_TIME)
    self.disp.setGameTimer(self.get_config('TIME', 'GAME_TIME', type=int, default=300))
    
    # self.disp.playAudio(self.get_config('MUSIC', 'START'))
    self.sleep(self.get_config('TIME', 'START_DELAY', type=int, default=1))

    plyrs = assignPlayers(int(form['playerCount']), self.manager)
    Q = questions.getQuestions(self.get_config('LINK', 'DB_URL'))
    P = cyclePlayers(plyrs)

    self.meta['score'] = 0

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
      
      if ans == '':
        self.disp.timeout()
      else:
        if question == ans:
          self.disp.setCorrect(ans)
          self.addScore(1)
        else:
          self.disp.doWrong()
          self.disp.setSelected(ans)
          self.addScore(-1)

      self.disp.setScore(self.meta['score'])

      # Step 4 disinvite player
      self.disp.flush()
      player.lightAll(False)
      # self.stopRound()
      self.sleep(self.get_config('TIME', 'BETWEEN_ROUNDS', type=int, default=1))

QuizShowGame()()