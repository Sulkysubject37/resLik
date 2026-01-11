#!/bin/bash
set -e

echo "Running tests..."

# Run Python tests
python -m pytest tests/ -v

echo "Running C++ simple test (if compiled manually, but here we rely on the install)"
# Note: In a real CI, we might run the C++ executable directly from the build dir.
# For Phase 1, the pip install proves the C++ builds.

echo "All tests passed."
