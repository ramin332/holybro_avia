from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='px4_remap',
            executable='imu_remap',
            name='imu_remap',
            output='screen'
        ),
        Node(
            package='px4_remap',
            executable='gps_remap',
            name='gps_remap',
            output='screen'
        ),
        Node(
            package='px4_remap',
            executable='odometry_remap',
            name='odometry_remap',
            output='screen'
        ),
        Node(
            package='px4_remap',
            executable='lidar_remap',
            name='lidar_remap',
            output='screen'
        ),
    ])
