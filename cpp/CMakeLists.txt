cmake_minimum_required(VERSION 3.15)
project(reslik_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# If pybind11_DIR is not set, try to find it normally
find_package(pybind11 CONFIG)

if(NOT pybind11_FOUND)
    message(WARNING "pybind11 not found via find_package. Standalone build might fail unless pybind11_DIR is provided.")
endif()

add_library(reslik_core
    src/reslik_unit.cpp
    src/normalization.cpp
    src/gating.cpp
    src/diagnostics.cpp
)

# Ensure the static library is built with PIC so it can be linked into the shared module
set_target_properties(reslik_core PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_include_directories(reslik_core PUBLIC include)

# Simple C++ test executable (no heavy test framework yet)
add_executable(test_reslik_cpp tests/test_reslik_unit.cpp)
target_link_libraries(test_reslik_cpp PRIVATE reslik_core)

add_executable(test_normalization tests/test_normalization.cpp)
target_link_libraries(test_normalization PRIVATE reslik_core)

# Python Bindings
pybind11_add_module(_core bindings/pybind_module.cpp)
target_link_libraries(_core PRIVATE reslik_core)

# Install the extension module into the python package
install(TARGETS _core DESTINATION reslik)

# Force CMake rebuild for v1.2.0