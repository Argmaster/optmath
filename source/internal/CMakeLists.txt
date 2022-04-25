cmake_minimum_required( VERSION 3.16 )
project( liboptmath CXX )

SET( CMAKE_CXX_STANDARD 17 )
SET( CMAKE_CXX_STANDARD_REQUIRED ON )
set( CMAKE_CXX_EXTENSIONS OFF )

# ---------------------------------------------------------------------------- #
#                   Add TBB (Intel Threaded Building Blocks)                   #
# ---------------------------------------------------------------------------- #

# find_package(TBB REQUIRED)

# -------------------------------------------------------------------------- #
#                        create optmath library binary                       #
# -------------------------------------------------------------------------- #
# find library sources
file( GLOB_RECURSE OPTMATH_SOURCE "source/*.c*" )
add_library( optmath STATIC ${OPTMATH_SOURCE} )
set_property( TARGET optmath PROPERTY POSITION_INDEPENDENT_CODE ON )

target_include_directories(
    optmath
    PRIVATE "include" "templates"
    )
set( OPTMATH_EXT_LIBS )
target_link_libraries( optmath ${OPTMATH_EXT_LIBS} )
# ---------------------------------------------------------------------------- #
#                        create test  suite for optmath                        #
# ---------------------------------------------------------------------------- #

set( OPTMATH_TEST_LIBS optmath ${OPTMATH_EXT_LIBS} )

create_tests(${PROJECT} ${PROJECT_SOURCE_DIR} ${OPTMATH_TEST_LIBS})
