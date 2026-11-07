IRIS AUV Stonefish Simulation Package (ROS 2)

Instructions

Tested on Ubuntu 24.04 with ROS 2 Jazzy and Stonefish 1.6.

1) Install ROS 2 Jazzy (https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html), including `ros-dev-tools`.

2) Clone the `jazzy` branch of the Stonefish fork outside your ROS workspace, then build and install it:

       sudo apt install libglm-dev libsdl2-dev libfreetype-dev libopengl-dev
       git clone -b jazzy https://github.com/lmbalves/stonefish.git
       cd stonefish && mkdir build && cd build
       cmake -DCMAKE_BUILD_TYPE=Release .. && make -j$(nproc)
       sudo make install && sudo ldconfig

    The Stonefish library and stonefish_ros2 must be the same version (currently 1.6.0).

    The fork is upstream Stonefish 1.6 (https://github.com/patrykcieslak/stonefish) plus a fix for the ocean surface shaders failing to link (`unresolved reference to function ShadingModel`) on some drivers, e.g. NVIDIA.

3) Create a workspace and clone the `jazzy` branches into `src/`:

       mkdir -p ~/iris_ws/src && cd ~/iris_ws/src
       git clone -b jazzy https://github.com/lmbalves/stonefish_ros2.git
       git clone -b jazzy https://github.com/lmbalves/iris_stonefish.git
       git clone -b jazzy https://github.com/lmbalves/iris_control.git

    The stonefish_ros2 fork is upstream 1.6.0 (https://github.com/patrykcieslak/stonefish_ros2) plus a compile fix for the event camera publisher and a resolvable PCL rosdep key.

4) Build the workspace (from `~/iris_ws`)

       source /opt/ros/jazzy/setup.bash
       rosdep install --from-paths src --ignore-src -y
       colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

To launch the simulation

    source install/setup.bash
    ros2 launch iris_stonefish iris_acoustic_full.launch.py

Notes

- Stonefish 1.6 loads meshes with rapidobj, which fails on `mtllib`/`usemtl` references to missing `.mtl` files. Those lines are commented out in `data/` meshes; do the same for any new OBJ exported without its material file.
- The legacy ROS 1 launch files (`*.launch`) are kept for reference only.
