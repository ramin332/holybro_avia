# package_b/launch/main_launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource, FrontendLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
from datetime import datetime

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package='holybro_prep').find('holybro_prep')
    rviz_config_path = os.path.join(pkgPath, 'rviz', 'default_bag.rviz')
    bags_dir = '/home/avalor/holybro_avia/src/holybro_prep/bags'

    # Ensure the bags directory exists
    os.makedirs(bags_dir, exist_ok=True)

    # Create a timestamp for the bag file name
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    bag_file_path = os.path.join(bags_dir, f'rosbag2_{timestamp}')

    # Get the path to model launch directory
    model_launch = os.path.join(
        get_package_share_directory('holybro_model'),
        'launch',
        'holybro_model.launch.py'
    )

    # Get the path to lidar launch directory
    lidar_launch = os.path.join(
        get_package_share_directory('livox_ros2_avia'),
        'launch',
        'livox_lidar_launch.py'
    )


    # Get the path to remap launch directory (XML file)
    remap_launch = os.path.join(
        get_package_share_directory('px4_remap'),
        'launch',
        'remap.launch.py'
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]  
    )

    localization_launch = os.path.join(
        get_package_share_directory('holybro_localization'),
        'launch',
        'holybro_localization.launch.py'
    )

    vehicle_odom_to_tf = launch_ros.actions.Node(
        package='holybro_localization',
        executable='vehicle_odometry_to_tf',
        name='vehicle_odometry_to_tf',
        # parameters=[{'use_sim_time': True}]
    )

    # Static transform between 'map' and 'odom'
    static_transfer_1 = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher_map_to_odom',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
        # parameters=[{'use_sim_time': True}]
    )
    
    # ROS 2 bag recorder
    bag_recorder = ExecuteProcess(
        cmd=['ros2', 'bag', 'record', '-o', bag_file_path, '-a'],
        output='screen'
    )

    return LaunchDescription([
             IncludeLaunchDescription(
            PythonLaunchDescriptionSource(model_launch)
        ),

        # Include the lidar launch file (Python)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(lidar_launch)
        ),

        # Include the remap launch file (XML)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(remap_launch)
        ),

        # Include the localization launch file (XML)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(localization_launch)
        ),

        vehicle_odom_to_tf,
        static_transfer_1,
        # Start the ROS 2 bag recorder
        bag_recorder,
    ])
