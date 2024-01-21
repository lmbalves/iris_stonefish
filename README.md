IRIS AUV Stonefish Simulation Package

Instructions

This was tested in Ubuntu 20.04 without any known issues to this date.

1) Clone stonefish* to your home directory or any other (just not the catkin workspace you use for ROS), build and install on your machine following the instructions on https://stonefish.readthedocs.io/. 

    \* Version currently suported is 1.3. You can find a fork of the original repo used in https://github.com/lmbalves/stonefish.git freezed on that version.

    NOTE: in some machines you may need to run ldconfig in order to use stonefish after installing so $ sudo ldconfig

2) If you dont't have one already, create a catkin workspace

3) Clone stonefish_ros, there's also a fork of the original used in https://github.com/lmbalves/stonefish_ros.git

4) Clone this repo iris_stonefish into the workspace

Build the workspace

$ catkin build

To launch the simulation

roslaunch iris_stonefish iris_acustic_full.launch

or

roslaunch iris_stonefish iris_acoustic_no_gpu.launch
