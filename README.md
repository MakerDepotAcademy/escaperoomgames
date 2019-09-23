# Escape room games

This repo is a monolith for the escape room games. This is to allow better code sharing between games and ease of prototyping.

- [Escape room games](#escape-room-games)
  - [Architecture](#architecture)
  - [How to develop a new game](#how-to-develop-a-new-game)

## Architecture

The archetecture of the repo is meant to allow for encapsulation of various components of the games in a reusable fashion.

- /Root
  - [Components](Components) : where all the code shared by games goes
    - [game.py](Components/game.py) : The master game logic module
    - [board.py](Components/board.py) : The master gpio32 control module
    - [pause.py](Components/pause.py) : A semaphore used for pausing
    - [generic_display.py](Components/generic_display.py) : Contains the driver for interfacing with `/Display/Generic`
  - [Displays](Displays) : where all of the display programs are
    - [Quizshow-Display](Displays/Quizshow-Display) : The display program for quizshow
    - [Generic](Displays/Generic) : A generic display program
  - [Games](Games) : Where all the game logic and I/O interactions are defined
    - [Quizshow](Games/quizshow) : The quizshow game
    - [Feed The Animals](Games/feedtheanimals) : The "feed the animals" game
  - [Targets](Targets) : Where all the installation scripts will go (once I learn make)
    - ...

## How to develop a new game

1. Start by running the [start](Targets/newgame.sh) script
2. Define all the methods required by [`game.py`](Components/game.py)

