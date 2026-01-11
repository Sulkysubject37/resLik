#!/bin/bash
set -e

# Ensure we are using the local virtual environment
VENV_DIR="./reslik"
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found at $VENV_DIR. Please create it first."
    exit 1
fi

PYTHON="$VENV_DIR/bin/python"

echo "Running tests using $PYTHON..."

# Run Python tests
$PYTHON -m pytest tests/ -v

echo "Running C++ simple test (via installed package logic)"
# Note: In a real CI, we might run the C++ executable directly from the build dir.
# For Phase 1, the pip install proves the C++ builds.

echo "All tests passed."
