#!/bin/bash
# Comprehensive evaluation script for all documentation variants
# Evaluates core, full, mini, and slim test results

echo "Starting comprehensive evaluation of all documentation variants..."
echo ""

# Check if tests directory exists
if [ ! -d "tests" ]; then
    echo "Error: tests directory not found"
    exit 1
fi

# Check if ALL required files exist (in size order: mini -> slim -> core -> full)
MISSING_FILES=0
for variant in mini slim core full; do
    FILE="tests/test-llmdocs-jaseci-${variant}.txt"
    if [ ! -f "$FILE" ]; then
        echo "ERROR: Missing required file: $FILE"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

if [ $MISSING_FILES -gt 0 ]; then
    echo ""
    echo "All four test files (mini, slim, core, full) must be present to run evaluation."
    exit 1
fi

# Create reports directory if it doesn't exist
mkdir -p tests/reports

# Run the Python evaluation script
python3 evaluate_all.py

# Check if evaluation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "Evaluation completed successfully!"
    echo "Reports stored in tests/reports/"
    echo "Test results archived with timestamp in tests/"
else
    echo ""
    echo "Evaluation encountered errors"
    exit 1
fi
