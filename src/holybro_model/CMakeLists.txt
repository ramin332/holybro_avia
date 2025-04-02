cmake_minimum_required(VERSION 3.8)
project(holybro_model)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)
find_package(rviz2 REQUIRED)
find_package(robot_state_publisher REQUIRED)

# Install directories
install(DIRECTORY launch urdf meshes materials sdf urdf xacro rviz
  DESTINATION share/${PROJECT_NAME}
)

# Enable testing
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
