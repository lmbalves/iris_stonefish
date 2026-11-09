from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_estimator = LaunchConfiguration('use_estimator')
    radius = LaunchConfiguration('radius')

    return LaunchDescription([
        DeclareLaunchArgument('use_estimator', default_value='true',
                              description='true: range-only estimator + estimated_acoustic_pilot; '
                                          'false: original acoustic_pilot reading the USBL vector'),
        DeclareLaunchArgument('radius', default_value='3.0',
                              description='Orbit radius around the (real or virtual) tag [m]'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('stonefish_ros2'),
                    'launch',
                    'stonefish_simulator.launch.py'
                ])
            ]),
            launch_arguments={
                'simulation_data': PathJoinSubstitution([FindPackageShare('iris_stonefish'), 'data']),
                'scenario_desc': PathJoinSubstitution([FindPackageShare('iris_stonefish'), 'scenarios', 'iris_tank2.scn']),
                'simulation_rate': '100.0',
                'window_res_x': '1024',
                'window_res_y': '768',
                'rendering_quality': 'high',
                'robot_name': 'iris'
            }.items()
        ),

        # --- Range-only path: estimator -> /iris/tag_rel -> estimated pilot ---
        Node(
            package='iris_control',
            executable='tag_range_estimator',
            name='tag_range_estimator',
            output='screen',
            condition=IfCondition(use_estimator),
            parameters=[{
                'range_sigma': 0.1,
                'window': 40,
                'min_pings': 12,
                'converged_std': 0.3,
            }]
        ),
        Node(
            package='iris_control',
            executable='estimated_acoustic_pilot',
            name='estimated_acoustic_pilot',
            output='screen',
            condition=IfCondition(use_estimator),
            parameters=[{'radius': radius}]
        ),

        # --- Original path: pilot reads the full USBL vector ---
        Node(
            package='iris_control',
            executable='acoustic_pilot',
            name='acoustic_pilot',
            output='screen',
            condition=UnlessCondition(use_estimator),
            parameters=[{'radius': radius}]
        ),

        Node(
            package='iris_control',
            executable='thrust_setpoints_pub',
            name='thrust_setpoints_pub',
            parameters=[{'robot_name': 'iris'}]
        ),
    ])