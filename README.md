# Autobrake LiDAR Integration

This repository contains the code that will run on the Raspberry Pi during the Level 1 Autonomy Demo (Autobrake) on Saturday, Feb. 11. It leverages the [`rplidar_ros`](https://github.com/Slamtec/rplidar_ros) package and several custom nodes to output a `Boolean` value to the `/AEBLidar` topic when it should stop, and an `Int32` on the `/motion_command_vertical` and `/motion_command_horizontal` topics for controlling the brakes.

## Installation

1. Clone with submodules using `git clone --recursive <this repository>`

2. Make sure that `numpy` and `rospy` (and other dependencies) are installed and usable by `python3`

3. Run `catkin_make`

## Usage

1. Activate the catkin workspace with `source devel/setup.bash`

2. Start the LiDAR node (and initialize the `roscore`) and other nodes. If you don't want to have to `ssh` into a bunch of different windows, start these processes in the background by putting the ampersand (`&`) after them

   ```bash
   # read from the LiDAR
   roslaunch rplidar_ros rplidar_a1.launch &
   ```

   ```bash
   # output whether to break onto /AEBlidar
   rosrun inhouse_script emergency_brake.py &
   ```

   ```bash
   # joystick controller stuff
   roslaunch pacmod_game_control pacmod_game_control.launch &
   ```

   ```bash
   # start communication with the automation board
   rosrun rosserial_arduino serial_node.py /dev/ttyUSB1 &
   ```

   ```bash
   # final signal to ROSSerial
   rosrun inhouse_script final_cmd.py
   ```
