#!/usr/bin/env python3

import sys, os, time, signal
sys.path.append('./components')

from flask import Flask, request
from threading import Thread

import components.player as Player
import components.questions as Questions
import components.settings as Settings
from components.display import Display, displayQuestion
from components.pause import Pause

Times = Settings.Time()
Links = Settings.Links()
Scores = Settings.Scores()
Music = Settings.Music()
Scores.score = Scores.Init_Score

disp = Display(Links.Display_Host)
disp.setRoundTimer(Times.Round_Time)
disp.setGameTimer(Times.Game_Time)

def hook_pause(isPaused):
  pass
Pause = Pause(hook_pause)

def ambientAudioEnforcer():
  while True:
    disp.playAudio(Music.Ambient)
    sleep(Times.AmbientDelay)
ambinetAudioThread = Thread(target=ambientAudioEnforcer)

def gameLoop(pc):
  # Pregame prep
  disp.playAudio(Music.Start)
  sleep(Times.StartDelay)

  plyrs = Player.assignPlayers(pc)
  Q = Questions.getQuestions()
  P = Player.cyclePlayers(plyrs)
  while True:
    def round_tickdown(i):
      disp.setRoundTimer(i)

    # Match player to question
    question = next(Q)
    player = next(P)

    # Step 1: invite player
    Pause.block_if_paused()
    # player.flash(Times.Invite_Sleep)
    player.lightAll(True)
    disp.invitePlayer(player._id)
    disp.playAudio(Music.Start)

    # Step 2: Display question
    Pause.block_if_paused()
    question.show()
    displayQuestion(disp, question)

    # Step 3: Judge answer
    Pause.block_if_paused()
    ans = player.catchAnswer(round_tickdown)
    
    if ans == '':
      disp.timeout()
      disp.playAudio(Music.Wrong)
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
    Pause.block_if_paused()
    disp.flush()
    player.lightAll(False)
    time.sleep(Times.Invite_Sleep)


def gameTimeout():
  # This will nuke threads too, thanks brad
  i = Times.Game_Time
  while i > 0:
    Pause.block_if_paused()
    time.sleep(1)
    i -= 1
    disp.setGameTimer(i)

    if i == Music.WarningTime:
      disp.playAudio(Music.Warning)

    if i == 0:
      disp.playAudio(Music.End)
      for b in Player.Manager:
        b.reset()
      Player.Manager.closeall()
      os.kill(os.getpid(), signal.SIGQUIT)
      return
gameTimer = Thread(target=gameTimeout)

app = Flask(__name__)

@app.route('/start', methods=['POST'])
def flask_start_game():
  pc = request.form['playerCount']
  t = Thread(target=gameLoop, args=[int(pc)])
  t.start()
  gameTimer.start()
  ambinetAudioThread.start()
  return 'started'

@app.route('/pause')
def flask_pause_game():
  Pause.pause()
  if Pause.isPaused():
    return 'Game is paused'
  else:
    return 'Game is running'

@app.route('/score')
def flask_get_score():
  return str(Scores.score)

app.run(host='0.0.0.0', port=5000)