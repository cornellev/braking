#!/usr/bin/env bash
cd ~/catkin_ws
source ~/catkin_ws/devel/setup.bash
echo "123" | sudo chmod 666 /dev/ttyUSB0
roslaunch lidar_brake lidar.launch
