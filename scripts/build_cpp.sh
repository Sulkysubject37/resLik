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

# Use the venv's pip to install in editable mode with verbose output
$PIP install . -v

echo "Build complete."
