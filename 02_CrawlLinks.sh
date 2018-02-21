while read -r line
do
    wget $line.json
    sleep 30
done < links.txt