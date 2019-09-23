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

listener('round_time', '#round_time')
listener('game_time', '#game_time')
listener('score', '#score')
listenflash('roundsup')
listenflash('gameover')
listenflash('correct')