#!/bin/bash
set -e

echo "Building C++ core and Python bindings..."

# Use pip to install in editable mode with verbose output to see cmake logs
pip install . -v

echo "Build complete."
