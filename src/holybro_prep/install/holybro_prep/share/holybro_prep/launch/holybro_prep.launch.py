# package_b/launch/main_launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource, FrontendLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os
from launch.substitutions import Command, LaunchConfiguration
import launch_ros

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package='holybro_prep').find('holybro_prep')
    rviz_config_path = os.path.join(pkgPath, 'rviz', 'default.rviz')

    # Get the path to model launch directory
    model_launch = os.path.join(
        get_package_share_directory('holybro_model'),
        'launch',
        'holybro_model.launch.py'
    )

    # Get the path to lidar launch directory
    lidar_launch = os.path.join(
        get_package_share_directory('hps3d160_ros2'),
        'launch',
        'hps_camera.launch.py'
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

    # Static transform between 'map' and 'odom'
    static_transfer_1 = launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher_map_to_odom',
            output='screen',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
    )

    # Static transform between 'map' and 'odom'
    static_transfer_2 = launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher_map_to_odom',
            output='screen',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_link']
    )

    return LaunchDescription([
        # Include the model launch file (Python)
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
        # Start RViz
        rviz_node,
        static_transfer_1,
        static_transfer_2
    ])
