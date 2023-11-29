***AEB***

**Description**

This repo contains two packages that implement AEB using a Zed camera (auto_brake) and a rplidar module (lidar_brake)

**How to run**

*auto_brake*
1. Start roscore in a terminal with ```$roscore```
2. In a new terminal cd into this directory
3. Run '''./run_zed_brake_system.sh'''

*lidar_brake*
1. Start roscore in a terminal with ```$roscore```
2. In a new terminal cd into this directory
3. Run '''./run_lidar_brake_system.sh'''

**Topics published**

1. /AEBzed
   - std_msgs.Bool
   - True if object is closer than MINIMUM_DISTANCE
2. /AEBlidar
   - std_msgs.Bool
   - True if object is closer than MINIMUM_DISTANCE

**Troubleshooting**

1. Error: ```roscore cannot run as another roscore/master is already running.``` Solution: ```killall -9 rosmaster``` to kill the current roscore running in the background.
