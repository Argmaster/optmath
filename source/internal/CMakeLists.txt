cmake_minimum_required( VERSION 3.16 )
project( liboptmath CXX )

SET( CMAKE_CXX_STANDARD 17 )
SET( CMAKE_CXX_STANDARD_REQUIRED ON )
set( CMAKE_CXX_EXTENSIONS OFF )

# ---------------------------------------------------------------------------- #
#                   Add TBB (Intel Threaded Building Blocks)                   #
# ---------------------------------------------------------------------------- #

find_package(TBB REQUIRED)

# -------------------------------------------------------------------------- #
#                        create optmath library binary                       #
# -------------------------------------------------------------------------- #
# find library sources
file( GLOB_RECURSE OPTMATH_SOURCE "source/*.c*" )
add_library( optmath STATIC ${OPTMATH_SOURCE} )
target_include_directories(
    optmath
    PRIVATE "include"
    )
set( optmath_external TBB::tbb )
target_link_libraries( optmath ${optmath_external} )
# ---------------------------------------------------------------------------- #
#                        create test  suite for optmath                        #
# ---------------------------------------------------------------------------- #

set( optmath_test_libs optmath ${optmath_external} )

create_tests(${PROJECT} ${PROJECT_SOURCE_DIR} "include" ${optmath_test_libs})
