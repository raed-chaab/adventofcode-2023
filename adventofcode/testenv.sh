#!/usr/bin/env sh
# Helper script to bootstrap a local or okteto environment for development of test scripts.
set -eu

pip install --no-index --find-links vendor/ --requirement requirements.txt

pytest --setup-plan .

echo "=============================================================="
echo "Enable debug mode when testing with: ADVENTOFCODE_DEBUG=1"
echo "=============================================================="
