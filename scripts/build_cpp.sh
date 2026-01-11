#!/bin/bash
set -e

# Ensure we are using the local virtual environment
VENV_DIR="./reslik"
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found at $VENV_DIR. Please create it first."
    exit 1
fi

PYTHON="$VENV_DIR/bin/python"
PIP="$VENV_DIR/bin/pip"

# Force Apple Clang to avoid libc++ ABI mismatch with system Python
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++

echo "Building C++ core and Python bindings using $PYTHON..."

# Use the venv's pip to install in editable mode
$PIP install . -v

# Explicit C++ build for unit tests
mkdir -p cpp/build
pushd cpp/build
PYBIND11_CMAKEDIR=$(../../reslik/bin/python -m pybind11 --cmakedir)
cmake .. -DCMAKE_CXX_COMPILER=$CXX -DCMAKE_C_COMPILER=$CC -Dpybind11_DIR=$PYBIND11_CMAKEDIR
make -j4
popd

echo "Build complete."
