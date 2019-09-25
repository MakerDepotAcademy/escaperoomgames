# Components

- [Components](#components)
  - [`class Game(ABC)`](#class-gameabc)
    - [Fields](#fields)
    - [\_\_init\_\_(configpath)](#__init__configpath)
    - [gameLogic(form)](#gamelogicform)
    - [pause_change(paused)](#pause_changepaused)
    - [game_tick(time)](#game_ticktime)
    - [round_tick(time)](#round_ticktime)
    - [once_killed()](#once_killed)
    - [get_config(scope, args, default=None, type=str)](#get_configscope-args-defaultnone-typestr)
    - [kill(force=False)](#killforcefalse)
    - [killed()](#killed)
    - [block()](#block)
    - [sleep(t=1)](#sleept1)
    - [startRound()](#startround)
    - [stopRound()](#stopround)
    - [serve(port=5000)](#serveport5000)
      - [POST /start](#post-start)
      - [GET /pause](#get-pause)
      - [GET /dump](#get-dump)
      - [GET /kill](#get-kill)
  - [`class GameKilled(Exception)`](#class-gamekilledexception)
  - [`class Board()`](#class-board)
    - [Fields](#fields-1)
    - [\_\_init\_\_(port, qu=32, id=None)](#__init__port-qu32-idnone)
    - [close()](#close)
    - [flush()](#flush)
    - [run](#run)
    - [reset()](#reset)
    - [turnOn(pin)](#turnonpin)
    - [turnOf(pin)](#turnofpin)
    - [setInput(pin, inverse=False)](#setinputpin-inversefalse)
    - [unsetInput(pin, inverse=False)](#unsetinputpin-inversefalse)
    - [setInterrupt(pin, enabled=True)](#setinterruptpin-enabledtrue)
    - [getID()](#getid)
    - [getLocation()](#getlocation)
    - [getPorts()](#getports)
    - [awaitChange(pins, timeout, timeout_tick=None)](#awaitchangepins-timeout-timeout_ticknone)
  - [`class Manager()`](#class-manager)
    - [\_\_init\_\_(order)](#__init__order)
    - [\_\_getitem\_\_(i)](#__getitem__i)
    - [\_\_iter\_\_()](#__iter__)
    - [getBoardByID(i)](#getboardbyidi)
    - [closeall()](#closeall)
    - [resetall()](#resetall)
  - [`class Pause`](#class-pause)
    - [\_\_init\_\_(hook)](#__init__hook)
    - [block_if_paused()](#block_if_paused)
    - [isPaused()](#ispaused)
    - [pause()](#pause)
  - [`class Display()`](#class-display)
    - [\_\_init\_\_(address)](#__init__address)
    - [flush()](#flush-1)
    - [setRoundTime(t)](#setroundtimet)
    - [setGameTime(t)](#setgametimet)
    - [setScore(s)](#setscores)
    - [timeout()](#timeout)
    - [good()](#good)
    - [gameover()](#gameover)

## [`class Game(ABC)`](game.py)

`game.py` defines all of the I/O interractions with the game

### Fields

- manager : The gpio32 manager
- meta : a dict for storing metadata

### \_\_init\_\_(configpath)

Initalizes a Game instance 

- configpath <str> : The path to the config file

### gameLogic(form)

@abstractmethod

This is the actual game that will be run when the game starts

- form <dict> : A reference to the body of the start request

### pause_change(paused)

@abstractmethod

Is triggered when the game is paused/unpaused

- paused <bool> : `True` game has been paused, `False` game is being allowed to run

### game_tick(time)

@abstractmethod

Is triggered whenever the internal game timer changes

- time <int> : the current time logged by the timer

### round_tick(time)

@abstractmethod

Is triggered whenever the internal round timer changes

- time <int> : the current time logged by the timer

### once_killed()

@abstractmethod

Runs right before the game is killed

### get_config(scope, args, default=None, type=str)

Returns the value of a config element. If `default` is present, `default` will be returned in the absence of a value in the config file. If `type` is present, the value will be cast to that type. `default` must be of type `type`

- scope <str> : The name of the scope
- arg <str> : The key of the value
- default <any> : What to return if no value is avaliable
- type <type> : What to convert the value to
- returns: the requested value

### kill(force=False)

Marks the game for termination

- force <bool> : Kill the game now

### killed()

If `kill()` was run, this function will actually kill the game and reset the board

### block()

Finds a reason to pause the game logic or kill the game

### sleep(t=1)

A custom sleep function that is affected by pausing and killing. Uses `block()`

- t <int> : how long to sleep for

### startRound()

Start's the internal round timer

### stopRound()

Stops the internal round timer

### serve(port=5000)

Serves an `http` endpoint for controlling the game

#### POST /start

Starts the game

#### GET /pause

Toggles the internal pausing mechanism

#### GET /dump

Dumps out the game's metadata

#### GET /kill

Safely kills the game

## [`class GameKilled(Exception)`](game.py)

A custom extension raised in the game logic when the game has been killed

## [`class Board()`](board.py)

### Fields

- queue : A list of the characters queued up to be sent on the serial

### \_\_init\_\_(port, qu=32, id=None)

Initalizes a new board manager

- port <str> : The name of the port to open (usually `/dev/ttyACM*`)
- qu <int> : how long the queue should be
- id <any> : vestigial, sometimes useful in debugging

### close()

Closes the serial connection

### flush()

Flushes the I/O

### run

Sends the queue to the serial and resets the queue

### reset()

Sends a series of reset commands to the serial

### turnOn(pin)

Turns on a pin

- pin <int> : which pin to turn on

### turnOf(pin)

Turns off a pin

- pin <int> : which pin to turn off

### setInput(pin, inverse=False)

Sets that pin to input

- pin <int> : which pin to set
- inverse <bool> : sets that pin to pull down

### unsetInput(pin, inverse=False)

Unsets that pin for inputting

- pin <int> : which pin to unset
- inverse <bool> : unsets that pin to pull down

### setInterrupt(pin, enabled=True)

Sets that pin to receive interrupts

- pin <int> : which pin to set
- enabled <bool> : wether to enable or disable interrupts

### getID()

Gets the ID of that board

- returns : the id

### getLocation()

Get's the location of that board

- returns : it's location

### getPorts()

Get's the current status of the pins

- returns : a string representing the status of each pin

### awaitChange(pins, timeout, timeout_tick=None)

Await's for a change on a set of pins. Return when one of the pins changes

- pins <list(int)> : the pins to monitor
- timeout <int> : how long to wait (seconds)
- timeout_tick <function(<int>)> : A function to be run every time the timer ticks down

## [`class Manager()`](board.py)

The manager for all connected boards

### \_\_init\_\_(order)

Initalizes every boards found @ `/dev/ttyACM0` then orders them according to `order`

- order <list> : An ordered list of board ids

### \_\_getitem\_\_(i)

Get's a board by it's position

- returns : a board

### \_\_iter\_\_()

Return's an iterator for all boards

- returns : an iterator

### getBoardByID(i)

Get's a board by it's position

- returns : a board

### closeall()

Closes all boards

### resetall()

Resets all boards

## [`class Pause`](pause.py)

A [semaphore](https://en.wikipedia.org/wiki/Semaphore_(programming)) used for pausing the game

### \_\_init\_\_(hook)

Initalizes a new pauser

- hook <function(<bool>)> : A function to be triggered by pausing

### block_if_paused()

Title.

### isPaused()

Tests if this is paused

- returns : a bool representing if this is paused

### pause()

Toggles the pause

## [`class Display()`](generic_display.py)

This is the driver for the [generic display](Displays/Generic)

### \_\_init\_\_(address)

Initalizes and connects to a display

- address <str> : the host for the display

### flush()

Sends the payload to the display

### setRoundTime(t)

Sets the round time display

- t <int> : The number to display

### setGameTime(t)

Sets the game time display

- t <int> : The number to display

### setScore(s)

Sets the score display

- t <int> : The number to display


### timeout()

Show the timeout message

### good()

Show the good message

### gameover()

Show the gameover message