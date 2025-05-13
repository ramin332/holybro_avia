# holybro_avia ROS2 Workspace

This repository contains a ROS2 workspace for the Holybro Avia drone, integrating LIDAR-based SLAM, localization, and PX4 autopilot communication. The workspace includes several ROS2 packages for sensor processing, 
LiDAR mapping, bridging a UDP message to a ROS2 service, and Holybro system bringup.

## Repository Structure

The `holybro_avia` workspace follows the standard ROS2 workspace layout:
- `src/`: Contains all ROS2 packages.
- `build/`, `install/`, `log/`: Generated during compilation (excluded via `.gitignore`).
- `build.sh`: Script to build the workspace.
- `record_bag.sh`: Script to record ROS2 bags for debugging or analysis

## Installation 

1. Clone the repository:
```bash
git clone https://github.com/your_username/holybro_avia.git
cd holybro_avia
```
2. Build the workspace:
```bash
./build.sh
```
3. Source the workspace:
```bash
source install/setup.bash
```
## Packages Overview
The workspace includes the following ROS2 packages in src/:

- **holybro_bringup**: Provides launch files and configurations to initialize the Holybro Avia system, integrating sensors and autopilot nodes.

- **holybro_localization**: Integrates GPS, IMU, and odometry data using `robot_localization` for sensor fusion, with launch files for EKF, NavSat Transform, and RViz visualization.

- **holybro_model**: Contains URDF/Xacro files, meshes, and RViz configurations for simulating and visualizing the Holybro Avia model.

- **holybro_prep**: Offers tools for environment setup, including static transforms, RViz visualization, and ROS bag recording for Holybro-based systems.

- **lidarslam_ros2**: Implements LIDAR-based SLAM using OpenMP-boosted GICP/NDT scan matching and graph-based backend for mapping and localization. A hard copy of the LIDAR-based SLAM package from:
https://github.com/rsasaki0109/lidarslam_ros2.

- **livox_ros2_avia**: A ROS2 driver for Livox Avia LIDAR, publishing point cloud data in custom or PointCloud2 formats, with RViz visualization support. A hard copy of the driver package from:
https://github.com/Livox-SDK/livox_ros_driver2.

- **mapping_bridge**: Bridges UDP socket messages to a ROS service to initiate mapping, enabling external control of the mapping process.
  
- **px4_remap**: Handles topic remapping and communication with the PX4 autopilot.
