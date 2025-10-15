cmake_minimum_required(VERSION 3.16.3)

project(learn_eigen)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE Release)


find_package(Eigen3 REQUIRED)
find_package(fmt REQUIRED)

add_executable(learn_eigen src/learn_eigen.cpp)
target_include_directories(learn_eigen PRIVATE ${CMAKE_SOURCE_DIR}/src)
target_link_libraries(learn_eigen Eigen3::Eigen fmt::fmt)