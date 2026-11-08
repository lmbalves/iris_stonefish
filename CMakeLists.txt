cmake_minimum_required(VERSION 3.10)
project(iris_stonefish)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(Stonefish REQUIRED)

# Prints mass, CG, CB, inertia and per-part placement of every robot link in a scenario.
# Usage: ros2 run iris_stonefish iris_mass_properties <data dir>/ <scenario.scn> [max parts]
add_executable(iris_mass_properties tools/iris_mass_properties.cpp)
target_compile_features(iris_mass_properties PUBLIC cxx_std_17)
target_link_libraries(iris_mass_properties Stonefish::Stonefish)
install(TARGETS iris_mass_properties DESTINATION lib/${PROJECT_NAME})

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
