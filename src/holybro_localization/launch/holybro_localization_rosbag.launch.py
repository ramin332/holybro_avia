# package_b/launch/main_launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource, FrontendLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os
from launch.substitutions import Command, LaunchConfiguration
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

    # Get the path to remap launch directory (XML file)
    remap_launch = os.path.join(
        get_package_share_directory('px4_remap'),
        'launch',
        'remap.launch.py'
    )

    # Get the path to remap launch directory (XML file)
    localization_launch = os.path.join(
        get_package_share_directory('holybro_localization'),
        'launch',
        'holybro_localization.launch.py'
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        #arguments=['-d', rviz_config_path]  
    )

    return LaunchDescription([
        # Include the model launch file (Python)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(model_launch)
        ),

        # Include the remap launch file (XML)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(remap_launch)
        ),
        # Include the remap launch file (XML)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(localization_launch)
        ),
        # Start RViz
        rviz_node,

    ])
