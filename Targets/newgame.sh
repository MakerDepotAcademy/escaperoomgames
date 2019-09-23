if [ -z "$1" ]
then 
  echo "Script requires the name of the game to initialize"
  exit 1
fi

GAME=Games/$1/$1.py
FOLDER=Games/$1

cd ..
mkdir -p $FOLDER
cp Targets/assets/gamedef.py $GAME
cp -r Targets/assets/components $FOLDER
sed -i "s/{{name}}/$1/" $GAME
git add $GAME
git commit $GAME -m "Initalized $1 game"
cd $FOLDER