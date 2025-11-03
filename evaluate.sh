#!/bin/bash
# Simple wrapper script to run Jac LLM benchmark evaluation

if [ $# -eq 0 ]; then
    echo "Usage: ./run_benchmark.sh <responses_file>"
    echo ""
    echo "Example:"
    echo "  ./run_benchmark.sh llm_responses.json"
    exit 1
fi

RESPONSES_FILE="$1"

# Check if file exists
if [ ! -f "$RESPONSES_FILE" ]; then
    echo "Error: File not found: $RESPONSES_FILE"
    exit 1
fi

# Run the benchmark
python3 jac_llm_benchmark.py "$RESPONSES_FILE"
