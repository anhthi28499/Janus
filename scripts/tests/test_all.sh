#!/bin/bash
# test_all.sh
set -e

echo "==============================="
echo "   Running All Test Suites"
echo "==============================="

# Make scripts executable before running
chmod +x scripts/tests/*.sh

./scripts/tests/test_be_unit.sh
./scripts/tests/test_be_integration.sh
./scripts/tests/test_fe_unit.sh

echo "==============================="
echo "   All tests passed!"
echo "==============================="
