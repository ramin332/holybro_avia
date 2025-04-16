from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    lidarslam_pkg = get_package_share_directory('lidarslam')
    localization_pkg = get_package_share_directory('holybro_localization')

    return LaunchDescription([
        ExecuteProcess(
            cmd=['ros2', 'run', 'mapping_bridge', 'udp_service_bridge'],
            output='screen'
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(lidarslam_pkg, 'launch', 'lidarslam.launch.py')
            )
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(localization_pkg, 'launch', 'holybro_localization_main.launch.py')
            )
        ),
    ])
