# holybro_localization

## Overview
The `holybro_localization` repository contains ROS2 configurations and launch files for localizing a Holybro-based robot. This package integrates sensor data from GPS, IMU, and odometry using the `robot_localization` package and provides tools for visualization and debugging through RViz.

---

## Directory Structure
```
.
├── CMakeLists.txt             # CMake configuration file
├── config/                    # Configuration files for localization
├── launch/                    # Contains ROS2 launch files
├── package.xml                # ROS2 package information
├── rviz/                      # RViz configuration files
├── src/                       # Source files for additional functionalities
```

---

## Installation

1. Navigate to the `src` directory of your ROS2 workspace:
   ```bash
   cd holybro_ws/src
   ```

2. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

3. Build the entire workspace:
   ```bash
   cd ..  # Navigate back to the workspace root
   colcon build
   source install/setup.bash
   ```

---

## Launch Files
The repository includes the following launch files:

### `holybro_localization.launch.py`
Runs the EKF and NavSat Transform nodes for sensor fusion.

#### Usage:
```bash
ros2 launch holybro_localization holybro_localization.launch.py
```

### `holybro_localization_main.launch.py`
Integrates localization with the Holybro model, LiDAR, and other components. Starts RViz and RViz Satellite.

#### Usage:
```bash
ros2 launch holybro_localization holybro_localization_main.launch.py
```

### `holybro_localization_rosbag.launch.py`
Launches the localization stack for use with a ROS bag file.

#### Usage:
```bash
ros2 launch holybro_localization holybro_localization_rosbag.launch.py
```

### `holybro_localization_odom.launch.py`
Launches the odometry-to-TF node and includes static transforms.

#### Usage:
```bash
ros2 launch holybro_localization holybro_localization_odom.launch.py
```

---

## Key Components

### EKF and NavSat Transform Nodes
- EKF Node: Provides sensor fusion for odometry, IMU, and GPS data.
- NavSat Transform Node: Integrates GPS data with IMU and odometry.

### RViz Configuration
- Located in `rviz/default.rviz`.
- Provides a visualization setup for analyzing localization performance.

### Source Files
- Custom nodes and utilities are located in the `src/` directory, including `vehicle_odometry_to_tf` for publishing odometry transforms.

---

## Requirements
- ROS2 Humble or later
- Python 3.8+
- RViz2 and RViz Satellite for visualization

---

## Debugging
Paths to configuration and RViz files are printed during launch for debugging purposes. Ensure the paths are correct and files are accessible.

---

## Contribution
Feel free to submit issues or pull requests for bug fixes, feature enhancements, or other contributions. Ensure your code adheres to the coding standards outlined in the repository.

---

## License
This repository is licensed under the terms specified in the `LICENSE` file.

---

## Acknowledgments
Thank you for using the `holybro_localization` package. For further support or inquiries, please contact the maintainers listed in the `package.xml` file.


