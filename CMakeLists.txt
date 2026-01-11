cmake_minimum_required(VERSION 3.15)
project(reslik LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Look for pybind11, which should be available in the build environment
find_package(pybind11 CONFIG)

if(NOT pybind11_FOUND)
    message(STATUS "pybind11 not found via find_package, assuming it will be handled by subdirectories or FetchContent in future phases.")
else()
    message(STATUS "Found pybind11: ${pybind11_VERSION}")
endif()

add_subdirectory(cpp)
