cmake_minimum_required(VERSION 3.15)
project(reslik_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# If pybind11_DIR is not set, try to find it normally
find_package(pybind11 CONFIG QUIET)

if(NOT pybind11_FOUND)
    message(STATUS "pybind11 not found via find_package. Attempting to locate via Python...")
    find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
    
    execute_process(
        COMMAND "${Python3_EXECUTABLE}" -m pybind11 --cmakedir
        OUTPUT_VARIABLE pybind11_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
        RESULT_VARIABLE _pybind11_cmd_status
    )

    if(NOT _pybind11_cmd_status EQUAL 0)
        # Fallback: try to guess standard location if command fails
        execute_process(
            COMMAND "${Python3_EXECUTABLE}" -c "import sys, os; print(os.path.join(sys.prefix, 'lib', 'python' + sys.version[:3], 'site-packages', 'pybind11', 'share', 'cmake', 'pybind11'))"
            OUTPUT_VARIABLE _guessed_dir
            OUTPUT_STRIP_TRAILING_WHITESPACE
        )
        if(EXISTS "${_guessed_dir}/pybind11Config.cmake")
            set(pybind11_DIR "${_guessed_dir}")
            set(_pybind11_cmd_status 0)
        endif()
    endif()
    
    if(_pybind11_cmd_status EQUAL 0 AND EXISTS "${pybind11_DIR}")
        message(STATUS "Found pybind11 via Python at: ${pybind11_DIR}")
        find_package(pybind11 CONFIG REQUIRED HINTS "${pybind11_DIR}")
    else()
        message(WARNING "Could not locate pybind11. Standalone build will fail unless pybind11_DIR is provided.")
    endif()
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
if(pybind11_FOUND)
    pybind11_add_module(_core bindings/pybind_module.cpp)
    target_link_libraries(_core PRIVATE reslik_core)

    # Install the extension module into the python package
    install(TARGETS _core DESTINATION reslik)
else()
    message(STATUS "Skipping python bindings build because pybind11 was not found.")
endif()

# Force CMake rebuild for v1.2.1