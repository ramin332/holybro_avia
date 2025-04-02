cmake_minimum_required(VERSION 3.8)
project(px4_remap)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(px4_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)

add_executable(imu_remap src/imu_remap.cpp)
ament_target_dependencies(imu_remap rclcpp px4_msgs sensor_msgs)
install(TARGETS imu_remap DESTINATION lib/${PROJECT_NAME})

add_executable(gps_remap src/gps_remap.cpp)
ament_target_dependencies(gps_remap rclcpp px4_msgs sensor_msgs)
install(TARGETS gps_remap DESTINATION lib/${PROJECT_NAME})

add_executable(odometry_remap src/odometry_remap.cpp)
ament_target_dependencies(odometry_remap rclcpp px4_msgs nav_msgs)
install(TARGETS odometry_remap DESTINATION lib/${PROJECT_NAME})

add_executable(lidar_remap src/lidar_remap.cpp)
ament_target_dependencies(lidar_remap rclcpp px4_msgs sensor_msgs)
install(TARGETS lidar_remap DESTINATION lib/${PROJECT_NAME})

# Install directories
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)
ament_package()
