from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument

def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('stonefish_ros2'),
                    'launch',
                    'stonefish_simulator.launch.py'
                ])
            ]),
            launch_arguments = {
                'simulation_data' : PathJoinSubstitution([FindPackageShare('iris_stonefish'), 'data']),
                'scenario_desc' : PathJoinSubstitution([FindPackageShare('iris_stonefish'), 'scenarios', 'iris_tank2.scn']),
                'simulation_rate' : '100.0',
                'window_res_x' : '800',
                'window_res_y' : '600',
                'rendering_quality' : 'low'
            }.items()
        )

        # # Launch control nodes
        # Node(
        #     package='iris_control',
        #     executable='acoustic_pilot',
        #     name='acoustic_pilot',
        #     parameters=[{'robot_name': iris}]
        # ),

        # Node(
        #     package='iris_control',
        #     executable='thrust_setpoints_pub',
        #     name='thrust_setpoints_pub',
        #     parameters=[{'robot_name': iris}]
        # )
    ])