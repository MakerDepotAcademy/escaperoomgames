# Quiz Show

This is the display component of the quiz show

- [Quiz Show](#quiz-show)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Websocket packet](#websocket-packet)

## Installation

``` bash
npm install
```

## Usage

All interactions are done via `websockets` on port `8080`

### Websocket packet

Posts new settings for the display. Setting are provided as a JSON object in the request body

```javascript
{
  'question': 'Set the question',
  'red': 'Set the red answer',
  'green': 'Set the green answer',
  'blue': 'Set the blue answer',
  'yellow': 'Set the yellow answer',
  'red.correct': 'Mark the red answer as correct',
  'green.correct': 'Mark the green answer as correct',
  'blue.correct': 'Mark the blue answer as correct',
  'yellow.correct': 'Mark the yellow answer as correct',
  'red.selected': 'Mark the red answer as selected',
  'green.selected': 'Mark the green answer as selected',
  'blue.selected': 'Mark the blue answer as selected',
  'yellow.selected': 'Mark the yellow answer as selected',
  'score.correct': 'Set the correct value',
  'score.wrong': 'Set the wrong value',
  'roundtick': 'Set the current round tick',
  'gametick': 'Set the current game tick',
  'roundsup': '',
  'gameover': '',
  'wrong': ''
  'videoplay': 'Play a video from the path you set here',
  'audioplay': 'Play audio from the path you set here'
}
```
