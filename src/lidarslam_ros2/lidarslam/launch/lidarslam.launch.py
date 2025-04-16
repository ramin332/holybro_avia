import os

import launch
import launch_ros.actions

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    main_param_dir = launch.substitutions.LaunchConfiguration(
        'main_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'param',
            'lidarslam.yaml'))
    
    rviz_param_dir = launch.substitutions.LaunchConfiguration(
        'rviz_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'rviz',
            'mapping.rviz'))

    # mapping = launch_ros.actions.Node(
    #     package='scanmatcher',
    #     executable='scanmatcher_node',
    #     parameters=[main_param_dir,{'use_sim_time': True}],
    #     remappings=[('/input_cloud','/lidar')],
    #     output='screen'
    #     )

    tf = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0','0','0','0','0','0','1','base_link','lidar_link'],
        parameters=[{'use_sim_time': True}]
        )
    
    lidarslam_node = launch_ros.actions.Node(
        package='lidarslam',
        executable='lidarslam',  
        parameters=[main_param_dir, {'use_sim_time': True}],
        remappings=[('/input_cloud','/lidar')],
        output='screen'
        )
    
    # graphbasedslam = launch_ros.actions.Node(
    #     package='graph_based_slam',
    #     executable='graph_based_slam_node',
    #     parameters=[main_param_dir,{'use_sim_time': True}],
    #     output='screen'
    #     )
    
    rviz = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_param_dir],
        parameters=[{'use_sim_time': True}]
        )


    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'main_param_dir',
            default_value=main_param_dir,
            description='Full path to main parameter file to load'),
        lidarslam_node,
        tf,
        rviz
    ])