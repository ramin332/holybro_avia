# holybro_prep

## Overview
The `holybro_prep` repository contains tools and configurations for preparing, recording, and visualizing Holybro-based ROS2 setups. It includes scripts for RViz visualization, static transforms, and ROS bag recording.

---

## Directory Structure
```
.
├── bags/                      # Directory for storing ROS bag files
├── CMakeLists.txt             # CMake configuration file
├── launch/                    # Contains ROS2 launch files
├── package.xml                # ROS2 package information
├── rviz/                      # RViz configuration files
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

### `holybro_play.launch.py`
Launches the Holybro model and RViz with remapped topics.

#### Usage:
```bash
ros2 launch holybro_prep holybro_play.launch.py
```

### `holybro_prep.launch.py`
Prepares the environment with static transforms, RViz, and additional nodes.

#### Usage:
```bash
ros2 launch holybro_prep holybro_prep.launch.py
```

### `holybro_rosbag.launch.py`
Records a ROS bag file while running the Holybro model and other nodes.

#### Usage:
```bash
ros2 launch holybro_prep holybro_rosbag.launch.py
```

---

## Key Components

### Static Transforms
- `static_transform_publisher` nodes establish fixed transformations between coordinate frames.

### RViz Configuration
- Default configurations for visualizing ROS2 topics are located in the `rviz/` directory.

### ROS Bag Recording
- The `holybro_rosbag.launch.py` file records all active topics to a timestamped bag file stored in the `bags/` directory.

---

## Requirements
- ROS2 Humble or later
- Python 3.8+
- RViz2 for visualization

---

## Debugging
Paths to RViz configurations and bag file directories are printed during launch for debugging purposes. Ensure the paths are correct and directories exist.

---

## Contribution
Feel free to submit issues or pull requests for bug fixes, feature enhancements, or other contributions. Ensure your code adheres to the coding standards outlined in the repository.

---

## License
This repository is licensed under the terms specified in the `LICENSE` file.

---

## Acknowledgments
Thank you for using the `holybro_prep` package. For further support or inquiries, please contact the maintainers listed in the `package.xml` file.


