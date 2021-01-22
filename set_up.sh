#!/bin/sh

echo "Set up Now!"
cd ..
mkdir LiDAR_data
cd LiDAR_data
mkdir Sequence1a
cd Sequence1a
for i in `seq 14`
do
  if [ $i -le 9 ] ; then
    mkdir "LS_0$i"
    cd "LS_0$i"
    for j in `seq 0 1210`
    do
      if [ $j -le 9 ] ; then
        sed -e i "000${j}.csv"
        echo $j > "000${j}.csv"
      elif [ $j -le 99 ] ; then
        sed -e i "00${j}.csv"
        echo $j > "00${j}.csv"
      elif [ $j -le 999 ] ; then
        sed -e i "0${j}.csv"
        echo $j > "0${j}.csv"
      else
        sed -e i "${j}.csv"
        echo $j > "${j}.csv"
      fi
    done
    cd ..
  else
    mkdir "LS_$i"
    cd "LS_$i"
    for j in `seq 0 1210`
    do
      if [ $j -le 9 ] ; then
        sed -e i "000${j}.csv"
        echo $j > "000${j}.csv"
      elif [ $j -le 99 ] ; then
        sed -e i "00${j}.csv"
        echo $j > "00${j}.csv"
      elif [ $j -le 999 ] ; then
        sed -e i "0${j}.csv"
        echo $j > "0${j}.csv"
      else
        sed -e i "${j}.csv"
        echo $j > "${j}.csv"
      fi
    done
    cd ..
  fi
done
