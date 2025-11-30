#!/usr/bin/env python3

import os
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime

from condenser import LLMCondenser
from merger import DocumentMerger


def main():
    parser = argparse.ArgumentParser(
        description='Multi-stage merge pipeline for condensed documentation'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--input',
        type=str,
        help='Input directory (defaults to condensed output from config)'
    )
    parser.add_argument(
        '--ratio',
        type=int,
        help='Merge ratio override (e.g., 4 for 4:1)'
    )

    args = parser.parse_args()

    config_path = Path(__file__).parent.parent / args.config

    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}")
        return

    # Load config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    merge_config = config.get('merge', {})

    if not merge_config.get('enabled', False):
        print("Merge is not enabled in config. Set merge.enabled: true")
        return

    # Determine input directory
    if args.input:
        input_dir = Path(args.input)
    else:
        input_dir = Path(config['output_dir'])

    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        print("Run the condensation pipeline first: python3 pipeline.py")
        return

    # Determine merge ratio
    merge_ratio = args.ratio or merge_config.get('ratio', 4)

    # Output directory
    base_output_dir = Path(merge_config.get('output_dir', './output/merged'))
    base_output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize condenser and merger
    print("Initializing condenser...")
    condenser = LLMCondenser(config)

    print("Initializing merger...")
    merger = DocumentMerger(condenser)

    # Run multi-stage merge
    start_time = datetime.now()

    try:
        final_file = merger.run_multi_stage_merge(
            input_dir=input_dir,
            base_output_dir=base_output_dir,
            merge_ratio=merge_ratio,
            preserve_structure=merge_config.get('preserve_structure', True)
        )

        # Copy to final output name if specified
        final_output_name = merge_config.get('final_output', 'jac_documentation_final.txt')
        final_output_path = base_output_dir / final_output_name

        if final_file != final_output_path:
            import shutil
            shutil.copy(final_file, final_output_path)
            print(f"\nFinal document also saved as: {final_output_path}")

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # Get final file stats
        with open(final_output_path, 'r', encoding='utf-8') as f:
            final_content = f.read()
            final_chars = len(final_content)
            final_tokens = final_chars // 4

        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'input_dir': str(input_dir),
            'output_dir': str(base_output_dir),
            'merge_ratio': merge_ratio,
            'processing_time_seconds': processing_time,
            'final_file': str(final_output_path),
            'final_stats': {
                'chars': final_chars,
                'estimated_tokens': final_tokens
            }
        }

        report_path = base_output_dir / f"merge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nMerge report saved: {report_path}")
        print(f"\nFinal document stats:")
        print(f"  Characters: {final_chars:,}")
        print(f"  Estimated tokens: ~{final_tokens:,}")
        print(f"  Processing time: {processing_time:.2f}s")

    except Exception as e:
        print(f"\nError during merge: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == '__main__':
    main()
