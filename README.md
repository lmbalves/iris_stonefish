IRIS AUV Stonefish Simulation Package (ROS 2)

Instructions

Tested on Ubuntu 24.04 with ROS 2 Jazzy and Stonefish 1.6.

1) Install ROS 2 Jazzy (https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html), including `ros-dev-tools`.

2) Clone Stonefish (https://github.com/patrykcieslak/stonefish) outside your ROS workspace, then build and install it:

       sudo apt install libglm-dev libsdl2-dev libfreetype-dev libopengl-dev
       cd stonefish && mkdir build && cd build
       cmake -DCMAKE_BUILD_TYPE=Release .. && make -j$(nproc)
       sudo make install && sudo ldconfig

    The Stonefish library and stonefish_ros2 must be the same version (currently 1.6.0).

3) Create a workspace and clone into `src/`:
    - stonefish_ros2: https://github.com/patrykcieslak/stonefish_ros2
    - iris_stonefish (this repo) and iris_control: https://github.com/lmbalves/iris_control

4) Build the workspace

       source /opt/ros/jazzy/setup.bash
       rosdep install --from-paths src --ignore-src -y --skip-keys pcl
       colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

    (`--skip-keys pcl`: stonefish_ros2 declares a `pcl` rosdep key that doesn't resolve; `libpcl-dev` is installed with `ros-jazzy-pcl-conversions`.)

To launch the simulation

    source install/setup.bash
    ros2 launch iris_stonefish iris_acoustic_full.launch.py

Notes

- Stonefish 1.6 loads meshes with rapidobj, which fails on `mtllib`/`usemtl` references to missing `.mtl` files. Those lines are commented out in `data/` meshes; do the same for any new OBJ exported without its material file.
- The legacy ROS 1 launch files (`*.launch`) are kept for reference only.
