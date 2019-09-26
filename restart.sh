server_pid=$(jps | grep Reversi | awk '{print $1}')
human_pid=$(jps | grep Human | awk '{print $1}')
kill $human_pid $server_pid
echo "Killed processes $server_pid and $human_pid"

cd ReversiServer/
java Reversi 10 &
cd ../ReversiHuman/
java Human localhost 1 &
