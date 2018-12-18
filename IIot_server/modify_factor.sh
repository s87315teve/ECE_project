#!/bin/bash
#SERVER_PATH="./Dropbox/ZiQi_MengJie/To Dr. M. C. Chen/RVMcopy"
#pushd "$SERVER_PATH"
COLLECT_TIME=60
PROCESS_TIME=60
echo "1" > is_write.txt
# python test_server2.py &
for (( i=0; i<$COLLECT_TIME; i++ ))
do
	echo "."
	sleep 1;
done
echo "0" > is_write.txt
# pkill -1 -f test_server2.py;
python get_file.py 0 0 &
for (( i=0; i<$PROCESS_TIME; i++ ))
do
	sleep 1;
done
pkill -1 -f get_file.py;
cp log.csv server_file.csv
for FILE in "A0F0_ap"*
do
	echo $FILE
	python load_model.py $FILE server_file.csv;
	python training.py;
done

rm log.csv
rm A0F0_ap*
