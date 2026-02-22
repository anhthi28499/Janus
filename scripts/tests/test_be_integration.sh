#!/bin/bash
# test_be_integration.sh
echo "Running Backend Integration Tests..."

if [ ! -d "BE/venv" ]; then
    echo "Virtual environment not found. Please run 'make install' first."
    exit 1
fi

source BE/venv/bin/activate
pytest tests/BE/integration -v
