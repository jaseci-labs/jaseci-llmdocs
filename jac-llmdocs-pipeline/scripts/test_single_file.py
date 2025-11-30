#!/usr/bin/env python3

import os
import sys
import yaml
from pathlib import Path
from parser import DocumentParser
from condenser import LLMCondenser

def test_single_file():
    print("Testing Single File Condensation")
    print("=" * 80)

    test_file = "/home/kevinjin/jaseci-llmdocs/docs-new/learn/tool_suite.md"

    print(f"\nTest file: {test_file}")

    print("\n1. Parsing file...")
    parser = DocumentParser(
        source_dir="/home/kevinjin/jaseci-llmdocs/docs-new",
        skip_patterns=[]
    )

    doc_file = parser.parse_file(Path(test_file))
    print(f"   Sections found: {len(doc_file.sections)}")
    print(f"   Total chars: {doc_file.total_chars:,}")
    print(f"   Estimated tokens: ~{doc_file.total_chars // 4:,}")

    config_path = Path(__file__).parent.parent / "config" / "config_test.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    print("\n2. Initializing condenser...")
    try:
        condenser = LLMCondenser(config)
        print("   Condenser initialized successfully")
        print(f"   Provider: {config['llm']['provider']}")
        print(f"   Model: {config['llm']['model']}")
    except Exception as e:
        print(f"   ERROR: {e}")
        return False

    print("\n3. Condensing first section...")
    first_section = doc_file.sections[0]
    print(f"   Section: {first_section.section_title}")
    print(f"   Content length: {len(first_section.content)} chars")

    result = condenser.condense(first_section.content, first_section.section_title)

    if result.success:
        print(f"\n   SUCCESS!")
        print(f"   Original tokens:  ~{result.original_tokens:,}")
        print(f"   Condensed tokens: ~{result.condensed_tokens:,}")
        print(f"   Compression ratio: {result.compression_ratio:.2%}")
        print(f"   Processing time: {result.processing_time:.2f}s")

        print(f"\n   Original content (first 200 chars):")
        print(f"   {first_section.content[:200]}...")

        print(f"\n   Condensed content:")
        print(f"   {result.condensed_content}")

        is_valid = condenser.validate_result(result)
        print(f"\n   Validation: {'PASS' if is_valid else 'FAIL'}")

        return True
    else:
        print(f"\n   FAILED: {result.error}")
        return False

if __name__ == '__main__':
    try:
        success = test_single_file()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
