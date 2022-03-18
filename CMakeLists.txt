project(optmath_root CXX)
cmake_minimum_required(VERSION 3.16)

SET(CMAKE_CXX_STANDARD 17)
SET(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_BUILD_TYPE "Release")

add_subdirectory("source/internal")
