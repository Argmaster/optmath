cmake_minimum_required(VERSION 3.16)
cmake_policy(SET CMP0048 NEW)
project(optmath_root VERSION "1.0.0" LANGUAGES CXX)

SET(CMAKE_CXX_STANDARD 17)
SET(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# google test library setup
add_subdirectory(
    external/googletest
    )
enable_testing()
include_directories(
    external/googletest/include
    )
link_libraries(
    gtest_main
)
include(GoogleTest)

function(create_tests ROOT INCLUDE LIBRARIES)
    # Automatic test discovery function

    file(GLOB_RECURSE test_files "${ROOT}/tests/test_*.cpp")
    foreach(file ${test_files})
        get_filename_component(TEST_NAME ${file} NAME_WLE)
        add_executable(
            ${TEST_NAME}
            ${file}
        )
        target_include_directories(${TEST_NAME}
            PRIVATE
            ${INCLUDE}
        )
        target_link_libraries(${TEST_NAME}
            PRIVATE
            ${LIBRARIES}
        )
        gtest_discover_tests(${TEST_NAME})
    endforeach()
endfunction(create_tests)


add_subdirectory("source/internal")
