from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get package path
    pkg_share = get_package_share_directory('iris_stonefish')

    # Create launch configuration variables
    robot_name = LaunchConfiguration('robot_name')
    xacro_file = LaunchConfiguration('xacro_file')

    return LaunchDescription([
        DeclareLaunchArgument(
            'robot_name',
            default_value='iris',
            description='Robot name'
        ),
        
        DeclareLaunchArgument(
            'xacro_file',
            default_value=PathJoinSubstitution([
                pkg_share, 
                'data', 
                'urdf', 
                'iris.urdf.xacro'
            ]),
            description='Path to xacro file'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': Command(['xacro ', xacro_file, ' robot_namespace:=', robot_name]),
                'use_sim_time': True
            }],
            remappings=[
                ('robot_description', [robot_name, '/robot_description'])
            ]
        )
    ])