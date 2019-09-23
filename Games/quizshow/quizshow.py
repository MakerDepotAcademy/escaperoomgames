#!/usr/bin/env python3
import sys, os
sys.path.append('./components')
from components.game import Game

import player
import questions
from display import Display, displayQuestion

disp = None
class QuizShowGame(Game):

  def __init__(self):
    Game.__init__(self, os.getcwd() + '/config.cfg')

  def game_tick(self, time):
    disp.setGameTimer(time)

  def round_tick(self, time):
    disp.setRoundTimer(time)

  def once_killed():
    print('Killed')

  def pause_change(paused):
    print('Pause')
    print(paused)

  def gameLogic(self, form):
    # Pregame prep
    ROUND_TIME = self.get_config('TIME', 'ROUND', type=int, default=10)
    disp.setRoundTimer(ROUND_TIME)
    disp.setGameTimer(self.get_config('TIME', 'GAME', type=int, default=300))
    
    disp.playAudio(self.get_config('MUSIC', 'START'))
    self.sleep(self.get_config('TIME', 'START_DELAY', type=int))

    plyrs = Player.assignPlayers(self.manager, form['playerCount'])
    Q = Questions.getQuestions()
    P = Player.cyclePlayers(plyrs)
    while True:
      # Match player to question
      question = next(Q)
      player = next(P)

      # Step 1: invite player
      self.block()
      # player.flash(Times.Invite_Sleep)
      player.lightAll(True)
      disp.invitePlayer(player._id)
      disp.playAudio(START_MUSIC)
      # self.startRound()

      # Step 2: Display question
      self.block()
      question.show()
      displayQuestion(disp, question)

      # Step 3: Judge answer
      self.block()
      ans = player.catchAnswer(ROUND_TIME, self.round_tick)
      
      if ans == '':
        disp.timeout()
      else:
        if question == ans:
          disp.setCorrect(ans)
          Scores.score += Scores.Inc
        else:
          disp.doWrong()
          disp.setSelected(ans)
          Scores.score -= Scores.Dec

      disp.setScore(Scores.score)

      # Step 4 disinvite player
      disp.flush()
      player.lightAll(False)
      # self.stopRound()
      self.sleep(self.get_config('TIME', 'BETWEEN_ROUNDS'))

Q = QuizShowGame()
disp = Display(Q.get_config('LINK','DISP'), correct_music=Q.get_config('MUSIC', 'START'), wrong_music=Q.get_config('MUSIC', 'WRONG'))
Q.serve()