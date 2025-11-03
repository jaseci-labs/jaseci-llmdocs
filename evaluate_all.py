#!/usr/bin/env python3
"""
Comprehensive evaluation script for all documentation variants
Evaluates core, full, mini, and slim test results and generates a comparative report
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class MultiDocEvaluator:
    """Evaluates multiple documentation test results and generates comparison report"""

    VARIANTS = ['mini', 'slim', 'core', 'full']  # In increasing size order
    TESTS_DIR = Path('tests')
    REPORTS_DIR = TESTS_DIR / 'reports'
    RELEASE_DIR = Path('release')  # Original documentation files

    def __init__(self):
        self.results = {}
        self.file_sizes = {}
        # Create reports directory if it doesn't exist
        self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes"""
        if file_path.exists():
            return file_path.stat().st_size
        return 0

    def run_benchmark(self, variant: str) -> Dict:
        """Run benchmark for a specific variant"""
        file_name = f"test-llmdocs-jaseci-{variant}.txt"
        file_path = self.TESTS_DIR / file_name

        if not file_path.exists():
            print(f"Warning: {file_path} not found, skipping...")
            return None

        # Get file size from original documentation file in release/
        doc_file_name = f"llmdocs-jaseci-{variant}.txt"
        doc_file_path = self.RELEASE_DIR / doc_file_name
        file_size = self.get_file_size(doc_file_path)
        self.file_sizes[variant] = file_size

        # Run benchmark using jac_llm_benchmark.py
        print(f"Evaluating {variant}...")
        try:
            # Import and run benchmark directly to get structured results
            from jac_llm_benchmark import JacBenchmark
            benchmark = JacBenchmark()
            results = benchmark.run_benchmark(str(file_path))

            return results

        except json.JSONDecodeError as e:
            print(f"JSON error in {variant}: {e}")
            return None
        except Exception as e:
            print(f"Error evaluating {variant}: {e}")
            return None

    def check_all_files_exist(self) -> bool:
        """Check if all required test files exist"""
        missing = []
        for variant in self.VARIANTS:
            file_name = f"test-llmdocs-jaseci-{variant}.txt"
            file_path = self.TESTS_DIR / file_name
            if not file_path.exists():
                missing.append(variant)

        if missing:
            print("ERROR: Missing required test files:")
            for variant in missing:
                print(f"  - test-llmdocs-jaseci-{variant}.txt")
            print("\nAll four variants (core, full, mini, slim) must be present.")
            return False
        return True

    def evaluate_all(self):
        """Evaluate all variants"""
        print("=" * 80)
        print("MULTI-DOCUMENTATION EVALUATION")
        print("=" * 80)
        print()

        # Check all files exist first
        if not self.check_all_files_exist():
            sys.exit(1)

        for variant in self.VARIANTS:
            result = self.run_benchmark(variant)
            if result:
                self.results[variant] = result

        print()

    def generate_comparison_report(self):
        """Generate comprehensive comparison report"""
        if not self.results:
            print("No results to report")
            return

        print("=" * 80)
        print("COMPARATIVE ANALYSIS REPORT")
        print("=" * 80)
        print()

        # Summary Table
        print("SUMMARY TABLE")
        print("-" * 80)
        print(f"{'Variant':<12} {'Size (bytes)':<14} {'Score':<12} {'Max':<6} {'%':<8} {'Score/KB':<12}")
        print("-" * 80)

        summary_data = []
        for variant in self.VARIANTS:
            if variant in self.results:
                summary = self.results[variant]['summary']
                size = self.file_sizes[variant]
                score = summary['total_score']
                max_score = summary['total_max']
                percentage = summary['overall_percentage']
                score_per_kb = (score / (size / 1024)) if size > 0 else 0

                summary_data.append({
                    'variant': variant,
                    'size': size,
                    'score': score,
                    'max_score': max_score,
                    'percentage': percentage,
                    'score_per_kb': score_per_kb
                })

                print(f"{variant:<12} {size:<14} {score:<12.2f} {max_score:<6} {percentage:<8.2f} {score_per_kb:<12.2f}")

        print()

        # Efficiency Rankings
        print("EFFICIENCY RANKINGS (Score per KB)")
        print("-" * 80)
        ranked = sorted(summary_data, key=lambda x: x['score_per_kb'], reverse=True)
        for i, data in enumerate(ranked, 1):
            print(f"{i}. {data['variant']:<12} {data['score_per_kb']:>8.2f} score/KB "
                  f"({data['score']:.2f}/{data['max_score']} points, {data['size']} bytes)")
        print()

        # Absolute Score Rankings
        print("ABSOLUTE SCORE RANKINGS")
        print("-" * 80)
        ranked_score = sorted(summary_data, key=lambda x: x['score'], reverse=True)
        for i, data in enumerate(ranked_score, 1):
            print(f"{i}. {data['variant']:<12} {data['score']:>8.2f}/{data['max_score']} "
                  f"({data['percentage']:.2f}%)")
        print()

        # Category Comparison
        print("CATEGORY PERFORMANCE COMPARISON")
        print("-" * 80)

        # Get all categories
        categories = set()
        for variant in self.results:
            categories.update(self.results[variant]['summary']['category_breakdown'].keys())

        for category in sorted(categories):
            print(f"\n{category}:")
            print(f"  {'Variant':<12} {'Score':<12} {'Max':<6} {'%':<8}")
            for variant in self.VARIANTS:
                if variant in self.results:
                    cat_data = self.results[variant]['summary']['category_breakdown'].get(category)
                    if cat_data:
                        print(f"  {variant:<12} {cat_data['score']:<12.2f} "
                              f"{cat_data['max']:<6} {cat_data['percentage']:<8.2f}")

        print()

        # Level Comparison
        print("DIFFICULTY LEVEL COMPARISON")
        print("-" * 80)

        # Get all levels
        levels = set()
        for variant in self.results:
            levels.update(self.results[variant]['summary']['level_breakdown'].keys())

        for level in sorted(levels):
            print(f"\n{level}:")
            print(f"  {'Variant':<12} {'Score':<12} {'Max':<6} {'%':<8}")
            for variant in self.VARIANTS:
                if variant in self.results:
                    level_data = self.results[variant]['summary']['level_breakdown'].get(level)
                    if level_data:
                        print(f"  {variant:<12} {level_data['score']:<12.2f} "
                              f"{level_data['max']:<6} {level_data['percentage']:<8.2f}")

        print()

        # Size Analysis
        print("SIZE ANALYSIS")
        print("-" * 80)
        if self.file_sizes:
            total_size = sum(self.file_sizes.values())
            print(f"Total combined size: {total_size:,} bytes ({total_size/1024:.2f} KB)")
            print(f"\nSize distribution:")
            for variant in self.VARIANTS:
                if variant in self.file_sizes:
                    size = self.file_sizes[variant]
                    pct = (size / total_size * 100) if total_size > 0 else 0
                    print(f"  {variant:<12} {size:>8,} bytes ({pct:>5.1f}%)")

        print()

        # Best Performer Analysis
        print("BEST PERFORMER ANALYSIS")
        print("-" * 80)

        best_overall = max(summary_data, key=lambda x: x['score'])
        best_efficiency = max(summary_data, key=lambda x: x['score_per_kb'])
        smallest = min(summary_data, key=lambda x: x['size'])

        print(f"Highest Score:       {best_overall['variant']} ({best_overall['score']:.2f}/{best_overall['max_score']})")
        print(f"Most Efficient:      {best_efficiency['variant']} ({best_efficiency['score_per_kb']:.2f} score/KB)")
        print(f"Smallest Size:       {smallest['variant']} ({smallest['size']} bytes)")

        print()
        print("=" * 80)

        # Save detailed results to Markdown in reports directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.REPORTS_DIR / f"evaluation_report_{timestamp}.md"

        # Generate markdown report
        md_content = self.generate_markdown_report(summary_data, categories, levels)

        with open(output_file, 'w') as f:
            f.write(md_content)

        print(f"\nDetailed markdown report saved to: {output_file}")

        return timestamp

    def generate_markdown_report(self, summary_data: List[Dict], categories: set, levels: set) -> str:
        """Generate comprehensive markdown report"""
        md = []

        # Header
        md.append("# Jac Language Documentation Evaluation Report\n")
        md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md.append("---\n")

        # Executive Summary
        md.append("## Executive Summary\n")
        md.append("*Score/KB is calculated using the original documentation file size from release/.*\n")
        md.append("| Variant | Doc Size (KB) | Score | Max | Percentage | Score/KB |")
        md.append("|---------|---------------|-------|-----|------------|----------|")
        for data in summary_data:
            md.append(f"| {data['variant']} | {data['size']/1024:.2f} | {data['score']:.2f} | "
                     f"{data['max_score']} | {data['percentage']:.2f}% | {data['score_per_kb']:.2f} |")
        md.append("")

        # Efficiency Rankings
        md.append("## Efficiency Rankings (Score per KB)\n")
        ranked = sorted(summary_data, key=lambda x: x['score_per_kb'], reverse=True)
        for i, data in enumerate(ranked, 1):
            md.append(f"{i}. **{data['variant']}** - {data['score_per_kb']:.2f} score/KB "
                     f"({data['score']:.2f}/{data['max_score']} points, {data['size']:,} bytes)")
        md.append("")

        # Absolute Score Rankings
        md.append("## Absolute Score Rankings\n")
        ranked_score = sorted(summary_data, key=lambda x: x['score'], reverse=True)
        for i, data in enumerate(ranked_score, 1):
            md.append(f"{i}. **{data['variant']}** - {data['score']:.2f}/{data['max_score']} "
                     f"({data['percentage']:.2f}%)")
        md.append("")

        # Category Performance Comparison
        md.append("## Category Performance Comparison\n")
        for category in sorted(categories):
            md.append(f"### {category}\n")
            md.append("| Variant | Score | Max | Percentage |")
            md.append("|---------|-------|-----|------------|")
            for variant in self.VARIANTS:
                if variant in self.results:
                    cat_data = self.results[variant]['summary']['category_breakdown'].get(category)
                    if cat_data:
                        md.append(f"| {variant} | {cat_data['score']:.2f} | "
                                 f"{cat_data['max']} | {cat_data['percentage']:.2f}% |")
            md.append("")

        # Difficulty Level Comparison
        md.append("## Difficulty Level Comparison\n")
        for level in sorted(levels):
            md.append(f"### {level}\n")
            md.append("| Variant | Score | Max | Percentage |")
            md.append("|---------|-------|-----|------------|")
            for variant in self.VARIANTS:
                if variant in self.results:
                    level_data = self.results[variant]['summary']['level_breakdown'].get(level)
                    if level_data:
                        md.append(f"| {variant} | {level_data['score']:.2f} | "
                                 f"{level_data['max']} | {level_data['percentage']:.2f}% |")
            md.append("")

        # Size Analysis
        md.append("## Size Analysis\n")
        md.append("*Note: Sizes are of the original documentation files in release/, not test outputs.*\n")
        total_size = sum(self.file_sizes.values())
        md.append(f"**Total combined size:** {total_size:,} bytes ({total_size/1024:.2f} KB)\n")
        md.append("### Size Distribution\n")
        md.append("| Variant | Size (bytes) | Size (KB) | Percentage |")
        md.append("|---------|--------------|-----------|------------|")
        for variant in self.VARIANTS:
            if variant in self.file_sizes:
                size = self.file_sizes[variant]
                pct = (size / total_size * 100) if total_size > 0 else 0
                md.append(f"| {variant} | {size:,} | {size/1024:.2f} | {pct:.1f}% |")
        md.append("")

        # Best Performer Analysis
        md.append("## Best Performer Analysis\n")
        best_overall = max(summary_data, key=lambda x: x['score'])
        best_efficiency = max(summary_data, key=lambda x: x['score_per_kb'])
        smallest = min(summary_data, key=lambda x: x['size'])

        md.append(f"- **Highest Score:** {best_overall['variant']} "
                 f"({best_overall['score']:.2f}/{best_overall['max_score']})")
        md.append(f"- **Most Efficient:** {best_efficiency['variant']} "
                 f"({best_efficiency['score_per_kb']:.2f} score/KB)")
        md.append(f"- **Smallest Size:** {smallest['variant']} ({smallest['size']:,} bytes)")
        md.append("")

        # Detailed Breakdown by Variant
        md.append("## Detailed Breakdown by Variant\n")
        for variant in self.VARIANTS:
            if variant in self.results:
                md.append(f"### {variant.upper()}\n")
                summary = self.results[variant]['summary']
                md.append(f"- **Total Score:** {summary['total_score']}/{summary['total_max']} "
                         f"({summary['overall_percentage']:.2f}%)")
                md.append(f"- **Tests Completed:** {summary['tests_completed']}/{summary['tests_total']}")
                md.append(f"- **Documentation Size:** {self.file_sizes[variant]:,} bytes ({self.file_sizes[variant]/1024:.2f} KB)")
                md.append(f"- **Efficiency:** {summary['total_score'] / (self.file_sizes[variant] / 1024):.2f} score/KB")
                md.append("")

                # Category breakdown for this variant
                md.append("#### Category Scores")
                md.append("| Category | Score | Max | Percentage |")
                md.append("|----------|-------|-----|------------|")
                for cat, scores in summary['category_breakdown'].items():
                    md.append(f"| {cat} | {scores['score']:.2f} | {scores['max']} | "
                             f"{scores['percentage']:.2f}% |")
                md.append("")

        return "\n".join(md)

    def archive_results(self, timestamp: str):
        """Move test results to timestamped archive directory"""
        archive_dir = self.TESTS_DIR / timestamp
        archive_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nArchiving test results to {archive_dir}/")

        for variant in self.VARIANTS:
            file_name = f"test-llmdocs-jaseci-{variant}.txt"
            src = self.TESTS_DIR / file_name
            dst = archive_dir / file_name

            if src.exists():
                src.rename(dst)
                print(f"  Moved {file_name}")

        print("Archive complete!")


def main():
    evaluator = MultiDocEvaluator()
    evaluator.evaluate_all()
    timestamp = evaluator.generate_comparison_report()
    evaluator.archive_results(timestamp)


if __name__ == "__main__":
    main()
