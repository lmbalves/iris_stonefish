cmake_minimum_required(VERSION 3.8)
project(iris_stonefish)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

# Install launch and scenario files
install(DIRECTORY
  launch
  scenarios
  DESTINATION share/${PROJECT_NAME}
)

install(
  DIRECTORY data/
  DESTINATION share/${PROJECT_NAME}/data
)

ament_package()