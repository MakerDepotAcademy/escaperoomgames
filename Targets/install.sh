#!/usr/bin/env bash

ME=$0
TYPE=$1
THING=$2
ROOT=$(pwd)/..
ROOT=$(realpath $ROOT)
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
  REPLACE=$2
  echo "Installing service named $1"
  cd $ROOT/Targets/assets/selfupdater
  cp ./$NAME.service /etc/systemd/system/
  cd /etc/systemd/system/
  echo "Rewriting markers"
  python3 $ROOT/Targets/assets/selfupdater/findreplace.py $NAME.service $REPLACE
  chmod 644 $NAME.service
  echo "Enabling service ..."
  systemctl daemon-reload
  systemctl enable $NAME
  systemctl start $NAME
  echo "$1 service complete"
  cd $ROOT
}

function download_pip {
  echo "Downloading pip requirements"
  pip install -r requirements.txt
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
  if [ ! -d "$DDISPLAYS/$THING" ]
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
echo "Downloading requirements"
download_pip
install_service "self_updater" $ROOT

if [[ "$TYPE" == "game" ]]
then
  echo "Installing $THING game"
  cd $ROOT/Games/$THING
  if [ -a requirements.txt ]
  then
    download_pip
  fi
  install_service "game_runner" $ROOT/Games/$THING/$THING.py
fi

if [[ "$TYPE" == "display" ]]
then
  echo "Installing the $THING display"
  DISP=$DDISPLAYS/$THING
  cd $DISP
  npm install
  echo ". autostart" >> ~/.bashrc
  cd ~
  echo "export DISPLAY=:0" > autostart.sh
  echo "cd $DISP" > autostart.sh
  echo "screen -dms display npm start" >> autostart.sh
  chmod +x autostart.sh
  echo "Restart machine to load display"
fi
