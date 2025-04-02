cmake_minimum_required(VERSION 3.8)
project(holybro_localization)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(px4_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(geometry_msgs REQUIRED)

# Build the executable
add_executable(vehicle_odometry_to_tf src/vehicle_odometry_to_tf.cpp)

# Link dependencies to the executable
ament_target_dependencies(vehicle_odometry_to_tf
  rclcpp
  px4_msgs
  nav_msgs
  tf2_ros
  geometry_msgs
)

# Install the executable
install(TARGETS vehicle_odometry_to_tf
  DESTINATION lib/${PROJECT_NAME}
)

# Install directories
install(DIRECTORY launch rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
