option=$1
rm -f output.txt
touch output.txt

if [ $option -eq 1 ]; then
  cd DVR/Basic/ || exit
  touch output.txt
  python main.py
  cd ../
  output=`python basic.py`
  cd ../
  echo $output > output.txt
fi

if [ $option -eq 2 ]; then
  cd DVR/CountInf/ || exit
  python main.py
  cd ../
  output=`python countingInfinity.py`
  cd ../
  echo $output > output.txt
fi

if [ $option -eq 3 ]; then
  cd DVR/SplitHorizon/ || exit
  python main.py
  cd ../
  output=`python splitHorizon.py`
  cd ../
  echo $output > output.txt
fi

if [ $option -eq 4 ]; then
  cd LSR/Basic/ || exit
  python main.py
  cd ../
  output=`python basic.py`
  cd ../
  echo $output > output.txt
fi

