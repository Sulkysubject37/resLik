add_library(reslik_core
    src/reslik_unit.cpp
    src/normalization.cpp
    src/gating.cpp
    src/diagnostics.cpp
)

target_include_directories(reslik_core PUBLIC include)

# Simple C++ test executable (no heavy test framework yet)
add_executable(test_reslik_cpp tests/test_reslik_unit.cpp)
target_link_libraries(test_reslik_cpp PRIVATE reslik_core)

# Python Bindings
# pybind11 is provided by the environment (via pyproject.toml build-system)
pybind11_add_module(_core bindings/pybind_module.cpp)
target_link_libraries(_core PRIVATE reslik_core)

# Install the extension module into the python package
install(TARGETS _core DESTINATION reslik)
