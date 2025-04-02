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
    ])
