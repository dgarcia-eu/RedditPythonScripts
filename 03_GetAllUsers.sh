#!/bin/bash
FILES=*.json
rm usersns.txt
for f in $FILES
do
  python 03_GetUsers.py $f >> usersns.txt
done 

sort usersns.txt | uniq > users.txt
rm usersns.txt