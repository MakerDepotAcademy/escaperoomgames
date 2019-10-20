require('dotenv').config()

const { app, BrowserWindow, powerSaveBlocker } = require('electron')
const fs = require('fs')
const WebSocket = require('ws');
var player = require('play-sound')(opts = {})


var win

function updateUI(channel, msg, ws) {
  if (win) {
    win.webContents.send(channel, msg);
    console.log('UI', channel, msg)
    return true;
  }
  else {
    ws.send({
      'error': true,
      'msg': 'Display not working'
    })
    console.error('No display')
    return false;
  }
}

const wss = new WebSocket.Server({
  port: 8080,
  host: '0.0.0.0'
}, () => console.log('Listening on port 8080...'));

wss.on('connection', ws => {
  console.log('Connected')
  ws.on('message', msg => {
    console.log(msg)
    msg = JSON.parse(msg)
    for (let key in msg) {
      if (key == 'audioplay'){
        console.log('Playing ', msg[key])
        new Promise(resolve => {
          player.play(msg[key], { timeout: 300 }, function(err){
            if (err) throw err
            resolve(err)
          })
        })
        
        continue
      }
      if (key == 'restart'){
        updateUI('question', '', ws)
        updateUI('red', '', ws)
        updateUI('blue', '', ws)
        updateUI('green', '', ws)
        updateUI('yellow', '', ws)
        updateUI('gametick', '', ws)
        updateUI('roundtick', '', ws)
        updateUI('score.correct', '0', ws)
        updateUI('score.wrong', '0', ws)
        updateUI('gametick', '0', ws)
        updateUI('roundtick', '0', ws)
        continue
      }
      updateUI(key, msg[key], ws)
    }
  })
})

app.on('ready', () => {
  // Create the browser window.
  win = new BrowserWindow({
    width: 800,
    height: 600,
    frame: false,
    webPreferences: {
      nodeIntegration: true
    },
    webSecurity: false
  })
  win.webContents.openDevTools()
  win.maximize()
  win.setFullScreen(true)
  win.loadFile('app/index.html')
  const id = powerSaveBlocker.start('prevent-display-sleep')
  win.on('closed', () => {
    win = null
    powerSaveBlocker.stop(id)
  })
})

