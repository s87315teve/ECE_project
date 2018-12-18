#!/bin/bash
#SERVER_PATH="./Dropbox/ZiQi_MengJie/To Dr. M. C. Chen/RVMcopy"
#pushd "$SERVER_PATH"
COLLECT_TIME=60
PROCESS_TIME=30
echo "1" > is_write.txt
# python test_server2.py &
for (( i=0; i<$COLLECT_TIME; i++ ))
do
	echo "."
	sleep 1;
done
echo "0" > is_write.txt
# pkill -1 -f test_server2.py;
cp log.csv server_file.csv
python bin_packing.py
rm log.csv
