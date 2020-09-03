#!/bin/bash
echo "Run this script as root."

echo "18" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio18/direction
cd /home/dietpi/SmartFrame

while true; do
	HOUR=`date "+%-H"`
	if (($HOUR >= 8 && $HOUR <= 23)); then
		echo "Grabbing data and generating photo..."
		python3 SmartFramePhotoGen.py
		echo "Turning on frame..."
		echo "1" > /sys/class/gpio/gpio18/value
		sleep 5
		echo "Mounting frame..."
		mount /dev/sda1 /mnt
		echo "Wiping frame and sending photo..."
		rm -rf /mnt/*
		cp SmartFramePhoto.jpg /mnt
		sleep 1
		echo "Umounting frame..."
		umount /mnt
		echo "Turning off frame..."
		echo "0" > /sys/class/gpio/gpio18/value
		echo "Frame Updated!"
	fi
	echo "HOUR = $HOUR"
	echo "Sleeping..."
	sleep 30
done
