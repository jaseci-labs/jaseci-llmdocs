#!/bin/bash

# clean_doc.sh - Remove blank lines from documentation files
# Usage: ./clean_doc.sh <file> [-i]
#   -i: modify file in-place

if [ $# -eq 0 ]; then
    echo "Usage: $0 <file> [-i]"
    echo "  -i: modify file in-place"
    exit 1
fi

FILE="$1"
INPLACE=false

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found"
    exit 1
fi

# Check for -i flag
if [ "$2" == "-i" ]; then
    INPLACE=true
fi

if [ "$INPLACE" = true ]; then
    # Modify in-place
    sed -i '/^$/d' "$FILE"
    echo "Cleaned: $FILE"
else
    # Output to stdout
    sed '/^$/d' "$FILE"
fi
