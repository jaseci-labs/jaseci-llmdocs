#!/usr/bin/env python3

import os
import json
import yaml
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from parser import DocumentParser, DocFile, DocSection
from condenser import LLMCondenser, CondensationResult
from merger import DocumentMerger


class CondensationPipeline:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.parser = DocumentParser(
            source_dir=self.config['source_dir'],
            skip_patterns=self.config['processing'].get('skip_patterns', [])
        )

        self.condenser = LLMCondenser(self.config)

        self.output_dir = Path(self.config['output_dir'])
        self.metrics_dir = Path(self.config['metrics_dir'])

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

        self.results = []
        self.errors = []

    def process_section(self, section: DocSection, file_rel_path: str) -> Dict:
        result = self.condenser.condense(section.content, section.section_title)

        return {
            'file': file_rel_path,
            'section': section.section_title,
            'start_line': section.start_line,
            'end_line': section.end_line,
            'level': section.level,
            'result': result
        }

    def process_file(self, doc_file: DocFile, parallel_sections: bool = False, section_workers: int = 4) -> List[Dict]:
        sections_to_process = [s for s in doc_file.sections if len(s.content.strip()) >= 50]

        if not sections_to_process:
            return []

        if parallel_sections and len(sections_to_process) > 1:
            # Process sections in parallel within this file
            results = []
            with ThreadPoolExecutor(max_workers=section_workers) as executor:
                future_to_section = {
                    executor.submit(self.process_section, section, doc_file.relative_path): section
                    for section in sections_to_process
                }

                for future in as_completed(future_to_section):
                    section = future_to_section[future]
                    try:
                        result_dict = future.result()
                        results.append(result_dict)

                        if not result_dict['result'].success:
                            self.errors.append({
                                'file': doc_file.relative_path,
                                'section': section.section_title,
                                'error': result_dict['result'].error
                            })

                    except Exception as e:
                        self.errors.append({
                            'file': doc_file.relative_path,
                            'section': section.section_title,
                            'error': str(e)
                        })
            return results
        else:
            # Process sections sequentially
            results = []
            for section in sections_to_process:
                try:
                    result_dict = self.process_section(section, doc_file.relative_path)
                    results.append(result_dict)

                    if not result_dict['result'].success:
                        self.errors.append({
                            'file': doc_file.relative_path,
                            'section': section.section_title,
                            'error': result_dict['result'].error
                        })

                except Exception as e:
                    self.errors.append({
                        'file': doc_file.relative_path,
                        'section': section.section_title,
                        'error': str(e)
                    })

            return results

    def save_condensed_file(self, doc_file: DocFile, section_results: List[Dict]):
        output_path = self.output_dir / doc_file.relative_path

        output_path.parent.mkdir(parents=True, exist_ok=True)

        condensed_sections = []
        for result_dict in section_results:
            if result_dict['result'].success:
                formatted = self.condenser.format_output(
                    result_dict['result'].condensed_content,
                    result_dict['section']
                )
                condensed_sections.append(formatted)

        if condensed_sections:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(condensed_sections))

    def run(self, parallel: bool = True, max_workers: int = 4, parallel_sections: bool = False, section_workers: int = 4):
        print("=" * 80)
        print("JAC LLM DOCUMENTATION CONDENSATION PIPELINE")
        print("=" * 80)
        print(f"Config: {max_workers} file workers, {section_workers} section workers per file")
        print(f"Parallel files: {parallel}, Parallel sections: {parallel_sections}")

        categories = self.config['processing'].get('categories')
        doc_files = self.parser.parse_all(categories=categories)

        stats = self.parser.get_statistics(doc_files)
        print(f"\nParsed {stats['total_files']} files:")
        print(f"  - {stats['total_sections']} sections")
        print(f"  - {stats['total_lines']:,} lines")
        print(f"  - ~{stats['estimated_tokens']:,} tokens")
        print(f"\nCategories: {stats['categories']}")
        print("\n" + "-" * 80)

        start_time = datetime.now()

        if parallel and len(doc_files) > 1:
            print(f"\nProcessing files in parallel (workers={max_workers})...")
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_file = {
                    executor.submit(self.process_file, doc_file, parallel_sections, section_workers): doc_file
                    for doc_file in doc_files
                }

                for future in tqdm(as_completed(future_to_file), total=len(doc_files)):
                    doc_file = future_to_file[future]
                    try:
                        section_results = future.result()
                        self.results.extend(section_results)
                        self.save_condensed_file(doc_file, section_results)
                    except Exception as e:
                        self.errors.append({
                            'file': doc_file.relative_path,
                            'error': str(e)
                        })
        else:
            print(f"\nProcessing files sequentially...")
            for doc_file in tqdm(doc_files):
                try:
                    section_results = self.process_file(doc_file, parallel_sections, section_workers)
                    self.results.extend(section_results)
                    self.save_condensed_file(doc_file, section_results)
                except Exception as e:
                    self.errors.append({
                        'file': doc_file.relative_path,
                        'error': str(e)
                    })

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        report = self.generate_report(stats, processing_time)

        return report

    def generate_report(self, input_stats: Dict, processing_time: float):
        successful_results = [r for r in self.results if r['result'].success]

        total_original_tokens = sum(r['result'].original_tokens for r in successful_results)
        total_condensed_tokens = sum(r['result'].condensed_tokens for r in successful_results)

        overall_ratio = total_condensed_tokens / total_original_tokens if total_original_tokens > 0 else 0

        report = {
            'timestamp': datetime.now().isoformat(),
            'input': input_stats,
            'processing': {
                'total_sections_processed': len(self.results),
                'successful': len(successful_results),
                'failed': len(self.errors),
                'processing_time_seconds': processing_time
            },
            'compression': {
                'original_tokens': total_original_tokens,
                'condensed_tokens': total_condensed_tokens,
                'compression_ratio': overall_ratio,
                'token_reduction': total_original_tokens - total_condensed_tokens,
                'reduction_percentage': (1 - overall_ratio) * 100
            },
            'errors': self.errors
        }

        report_path = self.metrics_dir / f"condensation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print("\n" + "=" * 80)
        print("CONDENSATION REPORT")
        print("=" * 80)
        print(f"\nProcessing completed in {processing_time:.2f}s")
        print(f"\nSections processed: {len(successful_results)} / {len(self.results)}")
        print(f"Errors: {len(self.errors)}")
        print(f"\nCompression Results:")
        print(f"  Original tokens:  ~{total_original_tokens:,}")
        print(f"  Condensed tokens: ~{total_condensed_tokens:,}")
        print(f"  Compression ratio: {overall_ratio:.2%}")
        print(f"  Token reduction:   ~{total_original_tokens - total_condensed_tokens:,} ({(1-overall_ratio)*100:.1f}%)")
        print(f"\nOutput directory: {self.output_dir}")
        print(f"Report saved: {report_path}")

        if self.errors:
            print(f"\nErrors encountered:")
            for error in self.errors[:5]:
                print(f"  - {error['file']}: {error.get('error', 'Unknown error')}")
            if len(self.errors) > 5:
                print(f"  ... and {len(self.errors) - 5} more")

        return report


def run_merge_stage(config: Dict, condenser: LLMCondenser) -> Path:
    """Run multi-stage merge on condensed output"""
    merge_config = config.get('merge', {})

    if not merge_config.get('enabled', False):
        print("\nMerge stage disabled in config (merge.enabled: false)")
        return None

    print("\n" + "=" * 80)
    print("STARTING MERGE STAGE")
    print("=" * 80)

    input_dir = Path(config['output_dir'])
    base_output_dir = Path(merge_config.get('output_dir', './output/merged'))
    merge_ratio = merge_config.get('ratio', 4)
    max_workers = merge_config.get('max_workers', 8)

    print(f"Merge workers: {max_workers} (concurrent group processing per stage)")

    merger = DocumentMerger(condenser)

    start_time = datetime.now()

    try:
        final_file = merger.run_multi_stage_merge(
            input_dir=input_dir,
            base_output_dir=base_output_dir,
            merge_ratio=merge_ratio,
            preserve_structure=merge_config.get('preserve_structure', True),
            max_workers=max_workers
        )

        # Copy to final output name
        final_output_name = merge_config.get('final_output', 'jac_documentation_final.txt')
        final_output_path = base_output_dir / final_output_name

        if final_file != final_output_path:
            shutil.copy(final_file, final_output_path)
            print(f"\nFinal document saved as: {final_output_path}")

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # Get final stats
        with open(final_output_path, 'r', encoding='utf-8') as f:
            final_content = f.read()
            final_chars = len(final_content)
            final_tokens = final_chars // 4

        # Generate merge report
        merge_report = {
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
            json.dump(merge_report, f, indent=2)

        print(f"\nMerge report saved: {report_path}")
        print(f"\nFinal document stats:")
        print(f"  Characters: {final_chars:,}")
        print(f"  Estimated tokens: ~{final_tokens:,}")
        print(f"  Processing time: {processing_time:.2f}s")

        return final_output_path

    except Exception as e:
        print(f"\nError during merge: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    parser = argparse.ArgumentParser(description='JAC Documentation Condensation & Merge Pipeline')
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--sequential',
        action='store_true',
        help='Process files sequentially instead of in parallel'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=16,
        help='Number of parallel workers (default: 16)'
    )
    parser.add_argument(
        '--condense-only',
        action='store_true',
        help='Only run condensation stage, skip merge'
    )
    parser.add_argument(
        '--merge-only',
        action='store_true',
        help='Only run merge stage, skip condensation'
    )

    args = parser.parse_args()

    config_path = Path(__file__).parent.parent / args.config

    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}")
        return

    # Load config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    parallel_sections = config['processing'].get('parallel_sections', False)
    section_workers = config['processing'].get('section_workers', 4)

    # Stage 1: Condensation
    if not args.merge_only:
        print("=" * 80)
        print("STAGE 1: CONDENSATION")
        print("=" * 80)

        pipeline = CondensationPipeline(str(config_path))
        condensation_report = pipeline.run(
            parallel=not args.sequential,
            max_workers=args.workers,
            parallel_sections=parallel_sections,
            section_workers=section_workers
        )
    else:
        # Check if condensed output exists
        output_dir = Path(config['output_dir'])
        if not output_dir.exists() or not list(output_dir.rglob("*.txt")):
            print(f"Error: No condensed output found in {output_dir}")
            print("Run without --merge-only first to generate condensed docs")
            return

        # Create condenser for merge stage
        pipeline = CondensationPipeline(str(config_path))

    # Stage 2: Merge
    if not args.condense_only:
        final_doc = run_merge_stage(config, pipeline.condenser)

        if final_doc:
            print("\n" + "=" * 80)
            print("PIPELINE COMPLETE")
            print("=" * 80)
            print(f"\nFinal ultra-condensed document: {final_doc}")
        else:
            print("\nMerge stage skipped or failed")
    else:
        print("\n" + "=" * 80)
        print("CONDENSATION COMPLETE")
        print("=" * 80)
        print(f"\nCondensed docs: {config['output_dir']}")


if __name__ == '__main__':
    main()
