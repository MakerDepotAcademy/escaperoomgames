const { ipcRenderer } = require("electron");

const listener = (channel, query, action) => {
  ipcRenderer.on(channel, (evt, arg) => {
    console.log(channel, arg)
    if (!action) {
      document.querySelector(query).textContent = arg;
    }
    else {
      action({
        'channel': channel,
        'query': query,
        'arg': arg
      })
    }
  });
};

const listenerAnswer = label => {
  let q = "#" + label + " #answer";
  listener(label, q);
  listener(label + ".correct", q, opts => {
    var c = document.querySelector('#correct')
    var e = document.querySelector(opts.query)
    c.classList.remove('hidden')
    e.innerText = '((' + e.innerText + '))'
    setTimeout(() => {
      c.classList.add('hidden')
    }, 1500);
  });

  listener(label + ".selected", q, opts => {
    var e = document.querySelector(opts.query)
    e.innerText = "** " + e.innerText + " **"
  })
};

const listenflash = (label, timeout=2000) => {
  ipcRenderer.on(label, (evt, arg) => {
    var e = document.querySelector('#' + label)
    e.classList.remove('hidden')
    setTimeout(() => {
      e.classList.add('hidden')
    }, timeout);
  });
}

listener('question', '#question');
listenerAnswer('red');
listenerAnswer('green');
listenerAnswer('blue');
listenerAnswer('yellow');
listener('roundtick', '#round_time');
listener('gametick', '#game_time');
listenflash('roundsup')
listenflash('gameover', 10000)
listenflash('wrong')
listenflash('player', 3000)
listenflash('timeout', 1000)

listener('score.correct', '#score.correct', (opts) => {
  let e = document.querySelector(opts.query)
  e.textContent = parseInt(e.textContent) + 1
});
listener('score.wrong', '#score.wrong', (opts) => {
  let e = document.querySelector(opts.query)
  e.textContent = parseInt(e.textContent) - 1
})

listener('player', '#player', opts => {
  var e = document.querySelector('#playername')
  e.innerText = opts.arg
})

var vid = document.querySelector('video')
vid.addEventListener('ended', () => {
  vid.classList.add('hidden')
  ipcRenderer.send('videodone')
})

ipcRenderer.on("videoplay", (evt, arg) => {
  vid.src = arg
  vid.classList.remove('hidden')
  vid.load()
  vid.play()
})
