cmake_minimum_required( VERSION 3.16 )
project( liboptmath CXX )

SET( CMAKE_CXX_STANDARD 17 )
SET( CMAKE_CXX_STANDARD_REQUIRED ON )
set( CMAKE_CXX_EXTENSIONS OFF )

# -------------------------------------------------------------------------- #
#                      find and incluse boost libraryies                     #
# -------------------------------------------------------------------------- #
# set( Boost_USE_STATIC_LIBS ON )
# set( Boost_USE_MULTITHREADED ON )
# set( Boost_USE_STATIC_RUNTIME ON )
#
# set( BOOST_ROOT "${PROJECT_SOURCE_DIR}/external/boost" )
# SET (BOOST_INCLUDEDIR "${PROJECT_SOURCE_DIR}/external/boost/include")
# SET (BOOST_LIBRARYDIR "${PROJECT_SOURCE_DIR}/external/boost/lib")
#
# add_subdirectory("${PROJECT_SOURCE_DIR}/external/boost" EXCLUDE_FROM_ALL)

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
set( optmath_external ""  ) # Boost::iterator
target_link_libraries( optmath ${optmath_external} )
# ---------------------------------------------------------------------------- #
#                        create test  suite for optmath                        #
# ---------------------------------------------------------------------------- #

set( optmath_test_libs optmath ${optmath_external} )

create_tests(${PROJECT} ${PROJECT_SOURCE_DIR} "include" ${optmath_test_libs})
