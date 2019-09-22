#!/usr/bin/env python3
sys.path.append('./components')
from components.game import Game

import player
import questions
from display import Display, displayQuestion

disp = None

class QuizShowGame(Game):

  def game_tick(self, time):
    disp.setGameTimer(time)

  def round_tick(self, time):
    disp.setRoundTimer(time)

  def gameLogic(self, form):
    # Pregame prep
    disp = Display(Links.Display_Host, correct_music=self.get_config('MUSIC', 'START'), wrong_music=self.get_config('MUSIC', 'WRONG'))
    disp.setRoundTimer(self.get_config('TIME', 'ROUND', type=int, default=10))
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
      self.startRound()

      # Step 2: Display question
      Pause.block_if_paused()
      question.show()
      displayQuestion(disp, question)

      # Step 3: Judge answer
      self.block()
      ans = player.catchAnswer()
      
      if ans == '':
        disp.timeout()
        disp.playAudio(self.get_config('MUSIC', 'WRONG'))
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
      self.stopRound()
      self.sleep(Times.Invite_Sleep)