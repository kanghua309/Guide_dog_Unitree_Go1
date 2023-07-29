#!/bin/bash


function killProsess() {
	NAME=$1
	echo $NAME
	PID=$(ps -e | grep $NAME | awk '{print $1}') 
	echo "PID: $PID"
	kill -9 $PID >/dev/null
}

function start() {
	echo "start"
	echo "----------------"
	rm -rf /tmp/.X11-unix/*
	echo "123456" | vncpasswd -f > /home/ros/.vnc/passwd
        chmod 0600 /home/ros/.vnc/passwd
	USER=root vncserver :1 -geometry 800x600 -depth  24
        websockify -D --web=/usr/share/novnc/ 8080 localhost:5901
}

function stop() {
	echo "stop"
	echo "----------------"
	killProsess "websockify"
        killProsess "Xtigervnc"
        rm /tmp/.X11-unix/* -rf
}

function restart() {
	echo "restart"
	echo "----------------"
	stop
	start
}

case "$1" in
	start )
		echo "****************"
		start
		echo "****************"
		;;
	stop )
		echo "****************"
		stop
		echo "****************"
		;;
	restart )
		echo "****************"
		restart
		echo "****************"
		;;
	* )
		echo "****************"
		echo "no command"
		echo "****************"
		;;
esac