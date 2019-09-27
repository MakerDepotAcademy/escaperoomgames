# quizshow

This is a quizshow

- [quizshow](#quizshow)
  - [Config file](#config-file)
  - [Display](#display)

## Config file

Paste this into `./config.cfg`

```conf
[TIME]
GAME_TIME=3
ROUND_TIME=10
BETWEEN_ROUNDS=1
START_DELAY=10

[BOARD]
STACK="10"

[DATABASE]
URL="sqlite:///quizShow.db"

[LINK]
DISP="localhost:8080"
DB_URL="sqlite:///quizShow.db"

[MUSIC]
START=""
CORRECT=""
WRONG=""
```

## Display

Docs can be found [here](../Display/README.md)
