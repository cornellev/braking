#!/usr/bin/env bash
echo "123" | sudo chmod 666 /dev/ttyUSB0
roslaunch lidar_brake lidar.launch
