"""Headless variant of iris_acoustic_full.launch.py.

Runs stonefish_simulator_nogpu (no window, no rendering) with iris_tank2_nogpu.scn, which is
the same world and vehicle without the cameras (console mode rejects vision sensors), plus the
same control nodes. Useful for control tests on machines without a GPU and for scripted runs.
"""
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('stonefish_ros2'),
                    'launch',
                    'stonefish_simulator_nogpu.launch.py'
                ])
            ]),
            launch_arguments={
                'simulation_data': PathJoinSubstitution([FindPackageShare('iris_stonefish'), 'data']),
                'scenario_desc': PathJoinSubstitution([FindPackageShare('iris_stonefish'), 'scenarios', 'iris_tank2_nogpu.scn']),
                'simulation_rate': '100.0',
            }.items()
        ),

        Node(
            package='iris_control',
            executable='acoustic_pilot',
            name='acoustic_pilot',
            parameters=[{'robot_name': 'iris'}]
        ),

        Node(
            package='iris_control',
            executable='thrust_setpoints_pub',
            name='thrust_setpoints_pub',
            parameters=[{'robot_name': 'iris'}]
        )
    ])
