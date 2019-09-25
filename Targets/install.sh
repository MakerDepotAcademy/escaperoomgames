#!/usr/bin/env bash

ME=$0
TYPE=$1
GAME=$2
ROOT=$(pwd)/..
DGAMES=$ROOT/Games
DDISPLAYS=$ROOT/Displays

function scan {
  find $1 -maxdepth 1 | grep -Po "(?<=\w\/)((\w|-|_)*)$"
}

function help {
  echo "Usage: $ME <game|display> [name]"
  echo ""
  echo "<game : Installs the game logic"
  echo "display> : Installs that game's display program"
  echo "[name] the name of the game to install"
  echo ""
  echo "Avaliable games:"
  scan $DGAMES
  echo ""
  echo "Avaliable displays:"
  scan $DDISPLAYS
  echo ""
  echo "Also installs background services to keep everything running" 
}

function error {
  echo "$ME: $1"
  help
  exit 1
}

if [[ -z $TYPE || -z $GAME ]]
then
  error "requires two arguments"
fi

if [[ "$TYPE" != "game" && "$TYPE" != "display" ]]
then
  error "first argument must be game or device"
fi

if [ $TYPE == "game" ]
then
  if [ ! -d "$DGAMES/$GAME" ]
  then
    error "Game does not exist"
  fi
fi

if [ $TYPE == "display" ]
then
  if [ ! -d "$DDISPLAY/$GAME" ]
  then
    error "Display does not exist"
  fi
fi

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 
  exit 1
fi

