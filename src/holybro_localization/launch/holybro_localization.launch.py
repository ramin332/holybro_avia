from launch import LaunchDescription
from launch_ros.actions import Node

# EKF Localization Node
# ekf = Node(
#     package='robot_localization',
#     executable='ekf_node',
#     name='ekf_filter_node',
#     output='screen',
#     parameters=['/home/avalor/ros2_ws/src/holybro_localization/config/holybro_localization.yaml'],
#     remappings=[
#         ('/odometry/filtered', '/odometry/ekf')  # Unieke output topic
#     ]
# )

# Navsat Transform Node for GPS integration
# navsat = Node(
#     package='robot_localization',
#     executable='navsat_transform_node',
#     name='navsat_transform_node',
#     output='screen',
#     parameters=['/home/avalor/ros2_ws/src/holybro_localization/config/holybro_localization.yaml'],
#     remappings=[
#         ('imu', '/imu'),
#         ('gps/fix', '/gps/fix'),
#         ('odometry/filtered', '/odometry'),  # Gebruik ruwe odometrie
#         ('odometry/gps', '/odometry/gps')
#     ]
# )

def generate_launch_description():
    return LaunchDescription([
        # ekf,
        # navsat
    ])