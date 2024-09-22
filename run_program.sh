#!/bin/bash

# Script to check for Python, install dependencies, and run the Python program

# Function to display error and exit
error_exit() {
    echo "[ERROR] $1"
    exit 1
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    error_exit "Python3 is not installed. Please install Python3 and try again."
fi

# Check if pygame is installed
if ! python3 -c "import pygame" &> /dev/null; then
    echo "[INFO] Installing pygame..."
    pip3 install pygame || error_exit "Failed to install pygame. Please check your environment."
fi

# Run the Python program
echo "[INFO] Running the program..."
python3 main.py

# Check if program execution succeeded
if [ $? -eq 0 ]; then
    echo "[INFO] Program ran successfully."
else
    error_exit "Program encountered an
