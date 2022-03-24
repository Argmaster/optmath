project(liboptmath CXX) cmake_minimum_required(VERSION 3.16)

    SET(CMAKE_CXX_STANDARD 17) SET(CMAKE_CXX_STANDARD_REQUIRED ON)
        set(CMAKE_BUILD_TYPE "Release")

            file(GLOB_RECURSE OPTMATH_SOURCE "source/*.c*")
                add_library(optmath STATIC ${OPTMATH_SOURCE})
                    target_include_directories(optmath PRIVATE "include")
