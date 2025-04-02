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
    bags_dir = '/home/avalor/ros2_ws/src/holybro_prep/bags'

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

    # ROS 2 bag recorder
    bag_recorder = ExecuteProcess(
        cmd=['ros2', 'bag', 'record', '-o', bag_file_path, '-a'],
        output='screen'
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
        # Start RViz
        rviz_node,
        # Start the ROS 2 bag recorder
        bag_recorder,
    ])
