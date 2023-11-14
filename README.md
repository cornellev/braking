***AEB***

**Description**

This repo contains two packages that implement AEB using a Zed camera (auto_brake) and a rplidar module (lidar_brake)

**How to run**

*auto_brake*
1. Source directory with ```source devel/setup.bash```
2. Start roscore with ```$roscore```
3. Start Zed_wrapper with ```$rosrun zed_wrapper zed_wrapper_node```
4. Stat zed_brake node with ```$roslaunch lidar_brake emergency_brake.launch```

*lidar_brake*
1. Source directory with ```source devel/setup.bash```
2. Start roscore with ```roscore```
3. Start rplidar with ```$roslaunch rplidar_ros rplidar_a1.launch```
4. Stat lidar_brake node with ```$roslaunch lidar_brake emergency_brake.launch```

**Topics published**

1. /AEBzed
   - std_msgs.Bool
   - True if object is closer than MINIMUM_DISTANCE
2. /AEBlidar
   - std_msgs.Bool
   - True if object is closer than MINIMUM_DISTANCE
**Troubleshooting**

1. Error: ```roscore cannot run as another roscore/master is already running.``` Solution: ```killall -9 rosmaster``` to kill the current roscore running in the background.
