#!/usr/bin/env bash

ME=$0
TYPE=$1
THING=$2
ROOT=$(pwd)/..
DGAMES=$ROOT/Games
DDISPLAYS=$ROOT/Displays

function scan {
  echo $(find $1 -maxdepth 1 | grep -Po "(?<=\w\/)((\w|-|_)*)$")
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
  echo "Also installs background services to keep every$THING running" 
}

function error {
  echo "$ME: $1"
  help
  exit 1
}

function install_service {
  NAME=$1
  cd $ROOT/Targets/assets/selfupdater
  cp ./$NAME.service /etc/systemd/system/
  cd /etc/systemd/system/
  sed -i 's/{{}}/$2/' $NAME.service
  service $NAME enable
  service $NAME start
  cd $ROOT
}

if [[ -z $TYPE || -z $THING ]]
then
  error "requires two arguments"
fi

if [[ "$TYPE" != "game" && "$TYPE" != "display" ]]
then
  error "first argument must be game or display"
fi

if [ $TYPE == "game" ]
then
  if [ ! -d "$DGAMES/$THING" ]
  then
    error "Game does not exist"
  fi
fi

if [ $TYPE == "display" ]
then
  if [ ! -d "$DDISPLAY/$THING" ]
  then
    error "Display does not exist"
  fi
fi

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 
  exit 1
fi

echo "Installing updater"
cd $ROOT/Targets/assets/selfupdater
pip3 install -r requirements.txt
install_service "self_updater" 

if [[ "$TYPE" == "game" ]]
then
  echo "Installing $THING game"
  cd $ROOT/Games/$THING
  if [ -a requirements.txt ]
  then
    pip3 install -r requirements.txt
  fi
  install_service "game_runner" $ROOT
fi

if [[ "$TYPE" == "display" ]]
then
  echo "Installing the $THING display"
  cd $ROOT/Displays/$THING
  npm install
  install_service "display_runner.service" $ROOT/Displays/$THING
fi
