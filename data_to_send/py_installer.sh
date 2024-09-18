#!/bin/bash

if command -v python3 &>/dev/null; then
    echo "Python is already installed."
else
    echo "Python is not installed. Please install Python manually."
    exit 1
fi

if ! python3 -m pip --version &>/dev/null; then
    echo "Pip is not installed. Installing pip..."
    python3 -m ensurepip --upgrade
    python3 -m pip install --upgrade pip
else
    echo "Pip is already installed."
fi

if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    python3 -m pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping package installation."
fi

echo "Done."
