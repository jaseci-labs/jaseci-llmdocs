#!/usr/bin/env python3

import os
import sys
from pathlib import Path

print("Testing Unified Pipeline Imports...")
print("=" * 80)

try:
    from parser import DocumentParser
    print("✓ DocumentParser imported")

    from condenser import LLMCondenser
    print("✓ LLMCondenser imported")

    from merger import DocumentMerger
    print("✓ DocumentMerger imported")

    print("\n" + "=" * 80)
    print("All imports successful!")
    print("\nThe unified pipeline is ready to run:")
    print("  python3 pipeline.py")
    print("\nOptions:")
    print("  python3 pipeline.py --condense-only   # Skip merge")
    print("  python3 pipeline.py --merge-only      # Skip condensation")
    print("  python3 pipeline.py --help            # Show all options")
    print("=" * 80)

except Exception as e:
    print(f"\n✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
