# quizshow

This is a quizshow

- [quizshow](#quizshow)
  - [Config file](#config-file)
  - [Display](#display)

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

[DATABASE]
URL="sqlite:///quizShow.db" # The database url

[LINK]
DISP="localhost:8080"
DB_URL="sqlite:///quizShow.db"

[VIDEOS]
SPLASH=""

[MUSIC]
START=""
CORRECT=""
WRONG=""
```

## Display

Docs can be found [here](../Display/README.md)
