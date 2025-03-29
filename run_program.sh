#!/bin/bash

# Script to install dependencies and run the Pygame maze game

# Define the Python script filename
PYTHON_SCRIPT="df_21.py"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
echo "Checking for Python installation..."
if ! command_exists python; then
    echo "Python not found. Attempting to install Python..."
    if command_exists winget; then
        winget install -e --id Python.Python.3.11
        echo "Refreshing environment. You may need to restart your shell after installation."
        export PATH="$PATH:/c/Python311:/c/Python311/Scripts"
    else
        echo "Error: winget not found. Please install Python manually from https://www.python.org/downloads/"
        exit 1
    fi
else
    echo "Python is already installed."
fi

# Verify Python version
PYTHON_VERSION=$(python --version 2>&1)
echo "Python version: $PYTHON_VERSION"

# Check if Pygame is installed
echo "Checking for Pygame..."
if python -c "import pygame" 2>/dev/null; then
    echo "Pygame is available."
else
    echo "Pygame not found. Installing Pygame..."
    python -m pip install pygame
    if [ $? -eq 0 ]; then
        echo "Pygame installed successfully."
    else
        echo "Error: Failed to install Pygame. Ensure pip is installed and try again."
        exit 1
    fi
fi

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: $PYTHON_SCRIPT not found in the current directory."
    echo "Please ensure the Python script is saved as $PYTHON_SCRIPT in $(pwd)"
    exit 1
fi

# Run the Python script
echo "Launching the Maze Game..."
python "$PYTHON_SCRIPT"

echo "Script execution completed."
