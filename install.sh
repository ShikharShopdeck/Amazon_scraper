#!/bin/bash

# Verify requirements.txt exists to prevent errors
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found in the current directory."
    echo "Please make sure you're running this script from your project root directory."
    exit 1
fi

# Install dependencies globally with upgrade flag
# The -U flag ensures packages are updated if they already exist
pipx install -U -r requirements.txt

# Check if the installation succeeded
if [ $? -eq 0 ]; then
    echo "All dependencies installed successfully!"
else
    echo "There was an error installing dependencies. Please check the error messages above."
    exit 1
fi