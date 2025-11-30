#!/usr/bin/env python3

import sys
from pathlib import Path
from parser import DocumentParser

def test_parser():
    print("Testing DocumentParser...")
    print("=" * 80)

    parser = DocumentParser(
        source_dir="/home/kevinjin/jaseci-llmdocs/docs-new",
        skip_patterns=["*.html", "*.css", "*.js", "index.md"]
    )

    print("\n1. Collecting markdown files...")
    files = parser.collect_markdown_files()
    print(f"   Found {len(files)} markdown files")

    print("\n2. Parsing first file...")
    if files:
        first_file = files[0]
        print(f"   File: {first_file}")
        doc_file = parser.parse_file(first_file)
        print(f"   Relative path: {doc_file.relative_path}")
        print(f"   Category: {doc_file.category}")
        print(f"   Sections: {len(doc_file.sections)}")
        print(f"   Total lines: {doc_file.total_lines}")
        print(f"   Total chars: {doc_file.total_chars}")

        print("\n   First 3 sections:")
        for i, section in enumerate(doc_file.sections[:3], 1):
            print(f"   {i}. {section.section_title} (L{section.start_line}-{section.end_line}, level {section.level})")
            print(f"      Content length: {len(section.content)} chars")

    print("\n3. Getting statistics for all files...")
    doc_files = parser.parse_all()
    stats = parser.get_statistics(doc_files)

    print(f"   Total files: {stats['total_files']}")
    print(f"   Total sections: {stats['total_sections']}")
    print(f"   Total lines: {stats['total_lines']:,}")
    print(f"   Total chars: {stats['total_chars']:,}")
    print(f"   Estimated tokens: ~{stats['estimated_tokens']:,}")
    print(f"   Categories: {stats['categories']}")

    print("\n" + "=" * 80)
    print("Parser test completed successfully!")

    return True

if __name__ == '__main__':
    try:
        success = test_parser()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
