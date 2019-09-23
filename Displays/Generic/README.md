# Quiz Show

This isa generic display

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
  'score': 'Set the score',
  'roundtick': 'Set the current round tick',
  'gametick': 'Set the current game tick',
  'roundsup': '',
  'gameover': '',
  'wrong': ''
}
```
