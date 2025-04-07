# package_b/launch/main_launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os
import launch_ros
from datetime import datetime

def generate_launch_description():
    # Get the path to the rviz config file
    pkgPath = launch_ros.substitutions.FindPackageShare(package='holybro_prep').find('holybro_prep')
    rviz_config_path = os.path.join(pkgPath, 'rviz', 'default_bag.rviz')

    # Get the path to model launch directory
    model_launch = os.path.join(
        get_package_share_directory('holybro_model'),
        'launch',
        'holybro_model.launch.py'
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

    return LaunchDescription([
        # Include the model launch file (Python)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(model_launch)
        ),
        # Include the remap launch file (Python)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(remap_launch)
        ),
        # RViz node
        rviz_node,
    ])
