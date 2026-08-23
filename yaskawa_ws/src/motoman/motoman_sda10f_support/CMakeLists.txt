cmake_minimum_required(VERSION 3.8)
project(motoman_sda10f_support)

find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)
find_package(motoman_resources REQUIRED)

install(DIRECTORY config launch meshes urdf
  DESTINATION share/${PROJECT_NAME})

ament_package()
