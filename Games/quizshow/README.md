# quizshow

This is a quizshow

- [quizshow](#quizshow)
  - [Setup](#setup)
  - [Config file](#config-file)
  - [Usage](#usage)
    - [QuizShowGamePlay.py](#quizshowgameplaypy)
    - [Display](#display)

## Setup

1. `pip3 install -r requirements.txt`
2. `cd Display && npm i`

## Config file

Paste this into `./config.cfg`

```conf
[TIME]
GAME_TIME=3
ROUND_TIME=10
INVITE_SLEEP=1

[BOARDS]
BOARD_STACK="10"
BOARD_PLAYER_LIMIT=4

[SCORES]
INC=1
DEC=1
INIT=0

[DATABASE]
URL="sqlite:///quizShow.db"

[LINKS]
DISP="localhost:8080"
ME="localhost:5000"
PREAMBLE_VID="./video.mp4"
AUDIO_FOLDER="./audio"

[MUSIC]
START=""
AMBIENT=""
WARNING=""
CORRECT=""
END=""
WRONG=""
```

## Usage

### QuizShowGamePlay.py

There are no CLI args

Api:

```bash
curl host.domain/start -X POST -d 'playerCount=#' # Starts a game
```

### Display

Docs can be found [here](../Display/README.md)
