#!/bin/bash

echo "Fixing dependency issues in the environment..."

# Upgrade pip
python -m pip install --upgrade pip

# Force reinstall the requirements
pip install --no-cache-dir --force-reinstall -r requirements.txt

# Verify numpy installation
echo "Verifying numpy installation:"
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"

echo "Dependencies have been updated. Please re-run your tests."
