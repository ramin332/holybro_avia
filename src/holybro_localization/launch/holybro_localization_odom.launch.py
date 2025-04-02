from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os
import launch_ros

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package='holybro_localization').find('holybro_localization')
    rviz_config_path = os.path.join(pkgPath, 'rviz', 'default.rviz')

    # Get the path to model launch directory
    model_launch = os.path.join(
        get_package_share_directory('holybro_model'),
        'launch',
        'holybro_model_rosbag.launch.py'
    )

    # Get the path to lidar launch directory
    lidar_launch = os.path.join(
        get_package_share_directory('livox_ros2_avia/livox_ros2_avia'),
        'launch',
        'livox_lidar_msg_launch.py'
    )

    # vehicle odom to tf
    vehicle_odom_to_tf = launch_ros.actions.Node(
        package='holybro_localization',
        executable='vehicle_odometry_to_tf',
        name='vehicle_odometry_to_tf',
        #parameters=[{'use_sim_time': True}]
    )

    # Static transform between 'map' and 'odom'
    static_transfer_1 = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher_map_to_odom',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
        #parameters=[{'use_sim_time': True}]
    )

    # RViz Node
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        #parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        # Include the model launch file (Python)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(model_launch)
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(lidar_launch)
        ),

        # Start odometry -> tf node
        vehicle_odom_to_tf,

        # map and odom should be fixed
        static_transfer_1,

        # Start RViz
        rviz_node,
    ])
