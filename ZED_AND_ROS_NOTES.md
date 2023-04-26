### Just a Quick Checklist of Things to do to get ros running


1. Initiate catkin. Create a catkin_ws/src/
2. Add required packages (adams' project and zed_wrapper) to /src/
3. In terminal, cd to catkin_ws . call catkin init
4. call catkin_make -DC_BUILD_TYPE=Release
5. source the project. call source ~/catkin_ws/devel/setup.bash
6. call rosrun and roslaunch. packages.... should show up.




### To Readd Packages
1. call catkin clean. if you haven't catkin init, it will give an error and do nothing
2. call catkin_make -DC_BUILD_TYPE=Release

### To Check if a Package is Available
1. call roscd [package name]
2. If it autocompletes your package, it is accessible.

### When the ZED fails to setup
1. Make sure you're using the main USB port. Not an adapter to the port. I think it requires USB 3.0 or something.
2. This happens fairly often. Keep just unplugging and replugging it and blowing air into the ports. And also wait a solid 20 seconds after unplugging it.
3. Try holding it in while it connects. might just hit a success. The USB port on the Xavier is loose/unstable.
