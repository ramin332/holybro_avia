from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os
import launch_ros
import launch

def generate_launch_description():
    rviz_param_dir = launch.substitutions.LaunchConfiguration(
        'rviz_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'rviz',
            'mapping.rviz'))
    
    model_launch = os.path.join(
        get_package_share_directory('holybro_model'),
        'launch',
        'holybro_model.launch.py'
    )

    lidar_launch = os.path.join(
        get_package_share_directory('livox_ros2_avia'),
        'launch',
        'livox_lidar_launch.py'
    )

    remap_launch = os.path.join(
        get_package_share_directory('px4_remap'),
        'launch',
        'remap.launch.py'
    )

    mapping_launch = os.path.join(
        get_package_share_directory('livox_ros2_avia'),
        'launch',
        'livox_lidar_launch.py'
    )

    main_param_dir = launch.substitutions.LaunchConfiguration(
        'main_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'param',
            'lidarslam.yaml'))

    mapping = launch_ros.actions.Node(
        package='scanmatcher',
        executable='scanmatcher_node',
        parameters=[main_param_dir],
        remappings=[('/input_cloud','/lidar')],
        output='screen'
        )

    tf = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0','0','0','0','0','0','1','base_link','lidar_link']
        )
    
    graphbasedslam = launch_ros.actions.Node(
        package='graph_based_slam',
        executable='graph_based_slam_node',
        parameters=[main_param_dir],
        output='screen'
        )
    
    # RViz Node
    rviz = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_param_dir]
        )

    # RViz Satellite Node
    rviz_satellite_node = launch_ros.actions.Node(
        package='rviz_satellite',
        executable='rviz_satellite',
        name='rviz_satellite',
        output='screen',
        parameters=[{
            'map_topic': '/satellite/map',  # Adjust topic if necessary
            'frame_id': 'map',             # Frame used for the satellite imagery
            'zoom': 17                     # Set zoom level; adjust as needed
        }]
    )

    vehicle_odom_to_tf = launch_ros.actions.Node(
        package='holybro_localization',
        executable='vehicle_odometry_to_tf',
        name='vehicle_odometry_to_tf',
        parameters=[{'use_sim_time': True}]
    )

    # Static transform between 'map' and 'odom'
    static_transfer_1 = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher_map_to_odom',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'main_param_dir',
            default_value=main_param_dir,
            description='Full path to main parameter file to load'),
        mapping,
        tf,
        graphbasedslam,
        # Include the model launch file (Python)
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(model_launch)
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(mapping_launch)
        ),
        
        # Include the lidar launch file (Python)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(lidar_launch)
        ),

        # Include the remap launch file (XML)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(remap_launch)
        ),

        # Start odometry -> tf node
        vehicle_odom_to_tf,

        # map and odom should be fixed
        static_transfer_1,

        # Start RViz
        rviz,

        # Start RViz Satellite
        # rviz_satellite_node,
    ])
