import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package='holybro_model').find('holybro_model')
    urdfModelPath= os.path.join(pkgPath, 'urdf/model_lidar.urdf')
    rviz_config_path = os.path.join(pkgPath, 'rviz', 'default.rviz')
    
    # Debugging: Print paths
    print(f"RViz config path: {rviz_config_path}")
    
    with open(urdfModelPath,'r') as infp:
    	robot_desc = infp.read()
    
    params = {'robot_description': robot_desc}
    
    robot_state_publisher_node =launch_ros.actions.Node(
    package='robot_state_publisher',
	executable='robot_state_publisher',
    output='screen',
    parameters=[params])
    
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]  
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='model', default_value=urdfModelPath,
                                            description='Path to the urdf model file'),
        robot_state_publisher_node,
        joint_state_publisher_node,
        # rviz_node
    ]) 
