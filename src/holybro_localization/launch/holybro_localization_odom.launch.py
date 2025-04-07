from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os
import launch_ros

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package='holybro_localization').find('holybro_localization')
    rviz_config_path = os.path.join(pkgPath, 'rviz', 'default.rviz')

    model_launch = os.path.join(
        get_package_share_directory('holybro_model'),
        'launch',
        'holybro_model_rosbag.launch.py'
    )

    lidar_launch = os.path.join(
        get_package_share_directory('livox_ros2_avia/livox_ros2_avia'),
        'launch',
        'livox_lidar_msg_launch.py'
    )

    vehicle_odom_to_tf = launch_ros.actions.Node(
        package='holybro_localization',
        executable='vehicle_odometry_to_tf',
        name='vehicle_odometry_to_tf',
        #parameters=[{'use_sim_time': True}]
    )

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

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(model_launch)
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(lidar_launch)
        ),

        vehicle_odom_to_tf,

        static_transfer_1,

        rviz_node,
    ])
