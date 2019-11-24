# quizshow

This is a quizshow

- [quizshow](#quizshow)
  - [Endpoints](#endpoints)
  - [Config file](#config-file)
  - [Display](#display)

## Endpoints

Quizshow only modifies one endpoint

POST /start: requires a form body 

```curl
playerCount=The number of players to enable
```

## Config file

Paste this into `./config.cfg`

```conf
[TIME]
GAME_TIME=3 # How long the game is
ROUND_TIME=10 # How long each round is
BETWEEN_ROUNDS=1 # A break between each round
START_DELAY=10 # How long to wait to play the game (set to the length of the splash video)

[BOARD]
STACK="10" # The order inwhich the gpio32 board ids should appear

[LINK]
DISP="localhost:8080" # The display host
DB_URL="sqlite:///quizShow.db" # The database url

[VIDEOS]
SPLASH="" # The splash video to run at the start

[MUSIC]
START="" # The start music
CORRECT="" # The correct tone
WRONG="" # The wrong tone
```

## Display

Docs can be found [here](../Display/README.md)
